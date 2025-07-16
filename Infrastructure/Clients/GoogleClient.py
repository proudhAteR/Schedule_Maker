from google.auth.transport.requests import Request

from Infrastructure.Clients.Client import Client


class GoogleClient(Client):
    def __init__(self, service: str):
        self.service = service
        super().__init__(
            'https://www.googleapis.com/auth/' + service,
            Request()
        )
