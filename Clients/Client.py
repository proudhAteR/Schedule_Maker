from aiohttp import ClientResponse as Response
from aiohttp import ClientSession as Session


class Client:
    def __init__(self, base_url: str, session: Session = None):
        self.base_url = base_url

        if not session:
            session = Session()
        self.session = session

    async def __aenter__(self):
        self.session = Session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def get(self, endpoint: str) -> Response:
        if not self.session:
            raise RuntimeError("Session not initialized")

        async with self.session.get(self.base_url + endpoint) as response:
            if response.status != 200:
                raise RuntimeError(f"Error fetching data: {response.status}")
            return response

    async def post(self, endpoint: str) -> Response:
        if not self.session:
            raise RuntimeError("Session not initialized")

        async with self.session.post(self.base_url + endpoint) as response:
            return response
