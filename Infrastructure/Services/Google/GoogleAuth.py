from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from Core.Interface.APIs.Auth import Auth
from Infrastructure.Clients.GoogleClient import GoogleClient
from Infrastructure.Services.Files.FileService import FileService
from ._internal.TokenHandler import TokenHandler
from ...Utils.Logs.Logger import Logger


class GoogleAuth(Auth):
    def __init__(self, client: GoogleClient, token_file: str = "google_token.json"):
        self.token_handler = TokenHandler(token_file, client)
        self.client = client
        self.config_name = "GOOGLE_CREDENTIALS"

    def run(self) -> Credentials:
        creds = self.token_handler.creds or self.token_handler.load()
        if not creds or not creds.valid:
            creds = self._process_token(creds)

        return creds

    def reconnect(self):
        if self.authenticated:
            self.token_handler.delete()

        return self.run()

    def _process_token(self, creds: Credentials | None) -> Credentials:
        if self.token_handler.refresh_needed(creds):
            try:
                creds = self.token_handler.refresh(creds)
            except Exception as e:
                Logger.warning(f"Token refresh failed: {e}")
                creds = self._run_auth_flow()
                self.token_handler.save(creds)
        else:
            creds = self._run_auth_flow()
            self.token_handler.save(creds)

        return creds

    def _run_auth_flow(self) -> Credentials:
        config = FileService.load_secret_config(self.config_name, "json")
        flow = InstalledAppFlow.from_client_config(config, self.client.scopes)
        return flow.run_local_server(port=0)

    @property
    def authenticated(self) -> bool:
        creds = self.token_handler.creds or self.token_handler.load()
        return creds is not None and creds.valid
