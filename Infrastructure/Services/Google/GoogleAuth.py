from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from Core.Interface.APIs.Auth import Auth
from Infrastructure.Clients.GoogleClient import GoogleClient
from Infrastructure.Utils.FileHandler import FileHandler
from Infrastructure.Utils.Logs.Logger import Logger


class GoogleAuth(Auth):
    def __init__(self, client: GoogleClient):
        self.token_path = FileHandler.secret_path('token.json')
        self.client = client

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
        self.__save_token(creds)
        return creds

    @staticmethod
    def __refresh_needed(creds: Credentials):
        return creds and creds.expired and creds.refresh_token

    def __load_token(self) -> Credentials | None:
        if FileHandler.exists(self.token_path):
            return Credentials.from_authorized_user_file(self.token_path, self.client.scopes)
        return None

    def __save_token(self, creds: Credentials):
        FileHandler.write(self.token_path, creds.to_json())

    def __run_auth_flow(self) -> Credentials:
        flow = InstalledAppFlow.from_client_config(
            FileHandler.get_env('GOOGLE_CREDENTIALS'), self.client.scopes
        )
        return flow.run_local_server(port=0)
