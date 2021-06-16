# pylint: disable=redefined-outer-name
import os
import asyncio
import json
import pytest
import aiohttp
import aiohttp.test_utils
from rctogether import RestApiSession


class CaseControlledTestServer(aiohttp.test_utils.RawTestServer):
    def __init__(self, **kwargs):
        super().__init__(self._handle_request, **kwargs)
        self._requests = asyncio.Queue()
        self._responses = {}  # {id(request): Future}

    async def close(self):
        """cancel all pending requests before closing"""
        for future in self._responses.values():
            future.cancel()
        await super().close()

    async def _handle_request(self, request):
        """push request to test case and wait until it provides a response"""
        self._responses[id(request)] = response = asyncio.Future()
        self._requests.put_nowait(request)
        try:
            # wait until test case provides a response
            return await response
        finally:
            del self._responses[id(request)]

    async def receive_request(self):
        """wait until test server receives a request"""
        return await asyncio.wait_for(self._requests.get(), 3)

    def send_response(self, request, *args, **kwargs):
        """send web response from test case to client code"""
        response = aiohttp.web.Response(*args, **kwargs)
        self._responses[id(request)].set_result(response)

    def create_request(self, coroutine):
        return RequestContext(self, coroutine)


@pytest.fixture
async def server():
    os.environ["RC_APP_ID"] = "1"
    os.environ["RC_APP_SECRET"] = "very_secret"

    async with CaseControlledTestServer() as test_server:
        os.environ["RC_ENDPOINT"] = f"http://localhost:{test_server.port}"
        yield test_server


@pytest.fixture
async def session():
    async with RestApiSession() as test_session:
        yield test_session


class RequestContext:
    def __init__(self, server, coroutine):
        self.task = asyncio.create_task(asyncio.wait_for(coroutine, 2))
        self.server = server
        self.response_sent = False
        self.request = None
        self.response = None

    async def __aenter__(self):
        print("Receiving request.")
        self.request = await self.server.receive_request()
        try:
            assert self.request.query["app_id"] == "1"
            assert self.request.query["app_secret"] == "very_secret"
        except:
            self.response.cancel()
            raise
        return self.request

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.task.cancel()
        else:
            if not self.response_sent:
                self.send_json({})
            self.response = await self.task

    def send_json(self, data):
        self.server.send_response(
            self.request, text=json.dumps(data), content_type="application/json"
        )
        self.response_sent = True
