import os
import aiohttp


class HttpError(Exception):
    pass


class RestApiSession:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.rc_app_id = os.environ["RC_APP_ID"]
        self.rc_app_secret = os.environ["RC_APP_SECRET"]
        self.rc_endpoint = os.environ.get(
            "RC_ENDPOINT", "https://recurse.rctogether.com"
        )

    async def __aenter__(self):
        self.session = await self.session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.__aexit__(exc_type, exc, tb)

    async def get(self, resource):
        async with self.session.get(url=self.api_url(resource)) as response:
            return await parse_response(response)

    async def delete(self, resource, resource_id, json=None):
        async with self.session.delete(
            url=self.api_url(resource, resource_id), json=json
        ) as response:
            return await parse_response(response)

    async def post(self, resource, json):
        async with self.session.post(url=self.api_url(resource), json=json) as response:
            return await parse_response(response)

    async def patch(self, resource, resource_id, json):
        async with self.session.patch(
            url=self.api_url(resource, resource_id), json=json
        ) as response:
            return await parse_response(response)

    def api_url(self, resource, resource_id=None):
        if resource_id is not None:
            resource = f"{resource}/{resource_id}"

        return f"{self.rc_endpoint}/api/{resource}?app_id={self.rc_app_id}&app_secret={self.rc_app_secret}"


async def parse_response(response):
    if response.status != 200:
        body = await response.text()
        raise HttpError(response.status, body)
    return await response.json()
