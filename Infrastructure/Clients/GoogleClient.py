from google.auth.transport.requests import Request
from Infrastructure.Clients.Client import Client


class GoogleClient(Client):
    def __init__(self, service: str):
        self.base_url = 'https://www.googleapis.com/auth/'
        self.service = service
        super().__init__(
            Request()
        )

    @property
    def scopes(self) -> list[str]:
        return [self.base_url + self.service]
