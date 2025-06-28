import aiohttp
from aiohttp import ClientResponse


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def get(self, endpoint: str) -> ClientResponse:
        if not self.session:
            raise RuntimeError("Session not initialized")

        async with self.session.get(self.base_url + endpoint) as response:
            if response.status != 200:
                raise RuntimeError(f"Error fetching data: {response.status}")
            return response

    async def post(self, endpoint: str) -> ClientResponse:
        if not self.session:
            raise RuntimeError("Session not initialized")

        async with self.session.post(self.base_url + endpoint) as response:
            return response