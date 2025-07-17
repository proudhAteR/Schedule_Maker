from Core.Interface.APIs.API import API
from google.auth.exceptions import TransportError
from googleapiclient.discovery import build

from Infrastructure.Clients.GoogleClient import GoogleClient
from Infrastructure.Services.Google.GoogleAuth import GoogleAuth


class GoogleAPI(API[GoogleClient]):
    def __init__(self, service: str):
        super().__init__(GoogleClient(service))

        try:
            self.authenticator = GoogleAuth(self.client)
            self.creds = self.authenticator.auth()
            self.resource = build(self.client.service, 'v3', credentials=self.creds)
        except (TransportError, FileNotFoundError) as e:
            raise ConnectionRefusedError(f'{e}')