from google.auth.exceptions import TransportError
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

from Core.Interface.APIs.API import API
from Infrastructure.Clients.GoogleClient import GoogleClient
from Infrastructure.Services.Google.GoogleAuth import GoogleAuth


class GoogleAPI(API[GoogleClient]):
    def __init__(self, service: str):
        super().__init__(
            GoogleClient(service)
        )

        try:
            self._authenticator = GoogleAuth(self.client)
            self._resource = build(
                self.client.service, 'v3', credentials=self._authenticator.run()
            )
        except (TransportError, FileNotFoundError) as e:
            raise ConnectionRefusedError(f'{e}')

    def _make_request(self, request: HttpRequest):
        return self.client.make_request(request)
