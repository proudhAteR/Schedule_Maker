from google.oauth2.credentials import Credentials

from Infrastructure.Clients.GoogleClient import GoogleClient
from Infrastructure.Services.Files.FileService import FileService


class TokenHandler:
    def __init__(self, token_file: str, client: GoogleClient):
        self.token_path =  FileService.secret_path(token_file)
        self.client = client
        self._creds: Credentials | None = None

    def load(self) -> Credentials | None:
        if not FileService.exists(self.token_path):
            return None
        self._creds = Credentials.from_authorized_user_file(self.token_path, self.client.scopes)
        return self._creds

    def save(self, creds: Credentials):
        FileService.write(self.token_path, creds.to_json())
        self._creds = creds

    def delete(self):
        FileService.delete(self.token_path)
        self._creds = None

    def refresh(self, creds: Credentials) -> Credentials:
        if self.refresh_needed(creds):
            try:
                creds.refresh(self.client.request)
                self.save(creds)
            except Exception as e:
                raise e

        return creds

    @staticmethod
    def refresh_needed(creds: Credentials | None) -> bool:
        return creds and creds.expired and creds.refresh_token

    @property
    def creds(self) -> Credentials | None:
        return self._creds
