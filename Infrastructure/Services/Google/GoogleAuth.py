from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from Core.Interface.APIs.Auth import Auth
from Infrastructure.Clients.GoogleClient import GoogleClient
from Infrastructure.Services.Files.FileService import FileService
from Infrastructure.Utils.Logs.Logger import Logger


class GoogleAuth(Auth):
    def __init__(self, client: GoogleClient, token: str = 'google_token.json'):
        self.token_path = FileService.secret_path(token)
        self.client = client
        self.config_name = "GOOGLE_CREDENTIALS"

    def auth(self) -> Credentials:
        creds = self.__load_token()
        if not creds or not creds.valid:
            creds = self.__process_token(creds)
        return creds

    def __process_token(self, creds: Credentials):
        if self.__refresh_needed(creds):
            try:
                creds.refresh(self.client.request)
            except Exception as e:
                Logger.warning(f"Token refresh failed: {e}")
                creds = self.__run_auth_flow()
        else:
            creds = self.__run_auth_flow()
        FileService.write(self.token_path, creds.to_json())
        return creds

    @staticmethod
    def __refresh_needed(creds: Credentials):
        return creds and creds.expired and creds.refresh_token

    def __load_token(self) -> Credentials | None:
        if FileService.exists(self.token_path):
            return Credentials.from_authorized_user_file(self.token_path, self.client.scopes)
        return None

    def __run_auth_flow(self) -> Credentials:
        config = FileService.load_secret_config(self.config_name, "json")
        flow = InstalledAppFlow.from_client_config(config, self.client.scopes)
        return flow.run_local_server(port=0)
