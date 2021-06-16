import os
import asyncio
import json
import pytest
import aiohttp
import aiohttp.test_utils
from rctogether import __version__, RestApiSession, bots, messages

class CaseControlledTestServer(aiohttp.test_utils.RawTestServer):
    def __init__(self, **kwargs):
        super().__init__(self._handle_request, **kwargs)
        self._requests = asyncio.Queue()
        self._responses = {}                # {id(request): Future}

    async def close(self):
        ''' cancel all pending requests before closing '''
        for future in self._responses.values():
            future.cancel()
        await super().close()

    async def _handle_request(self, request):
        ''' push request to test case and wait until it provides a response '''
        self._responses[id(request)] = response = asyncio.Future()
        self._requests.put_nowait(request)
        try:
            # wait until test case provides a response
            return await response
        finally:
            del self._responses[id(request)]

    async def receive_request(self):
        ''' wait until test server receives a request '''
        return await asyncio.wait_for(self._requests.get(), 3)

    def send_response(self, request, *args, **kwargs):
        ''' send web response from test case to client code '''
        response = aiohttp.web.Response(*args, **kwargs)
        self._responses[id(request)].set_result(response)

    def send_json(self, request, data):
        self.send_response(request, text=json.dumps(data), content_type="application/json")

@pytest.fixture
async def server():
    os.environ['RC_APP_ID'] = "1"
    os.environ['RC_APP_SECRET'] = "very_secret"

    async with CaseControlledTestServer() as server:
        os.environ['RC_ENDPOINT'] = f"http://localhost:{server.port}"
        yield server

@pytest.fixture
async def session():
    async with RestApiSession() as session:
        yield session


class RequestContext:
    def __init__(self, server, coroutine):
        self.response = asyncio.create_task(coroutine)
        self.server = server

    async def __aenter__(self):
        print("Receiving request.")
        request = await self.server.receive_request()
        try:
            assert request.query["app_id"] == "1"
            assert request.query["app_secret"] == "very_secret"
        except:
            self.response.cancel()
            raise
        return request

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.response.cancel()

def test_version():
    assert __version__ == '0.2.2'

@pytest.mark.asyncio
async def test_get_bots(server, session):
    request_context = RequestContext(server, bots.get(session))
    async with request_context as request:
        assert request.method == "GET"
        assert request.path == '/api/bots'

        server.send_json(request, [{'emoji': "🐙", 'name': "octopus"}])
    response = await request_context.response
    assert response == [{'emoji': "🐙", 'name': "octopus"}]

@pytest.mark.asyncio
async def test_send_message(server, session):
    request_context = RequestContext(server, messages.send(session, 17, "Hello, world"))
    async with request_context as request:
        assert request.method == "POST"
        assert request.path == '/api/messages'

        data = await request.json()

        assert data["bot_id"] == 17
        assert data["text"] == "Hello, world"

        server.send_json(request, [])

    response = await request_context.response
    assert response == []
