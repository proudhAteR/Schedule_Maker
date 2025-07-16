from Core.Interface.API import API
from google.auth.exceptions import TransportError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from Infrastructure.Clients.GoogleClient import GoogleClient
from Core.Models.Events.Event import Event
from Core.Models.Schedule import Schedule
from Infrastructure.Utils.FileHandler import FileHandler
from Infrastructure.Utils.Logger import Logger
import asyncio


class GoogleAPI(API):
    def __init__(self):
        try:
            self.client = GoogleClient('calendar')
            self.scopes = [self.client.base_url]
            self.creds = self.authenticate()
            self.res = build(self.client.service, 'v3', credentials=self.creds)
        except TransportError as e:
            Logger.error(f"Error while trying to authenticate : {e}")

    async def insert(self, event: Event, calendar_id: str = 'primary'):
        try:
            events = self.res.events()
            insert = events.insert(
                calendarId=calendar_id, body=event.to_google_event()
            )
            response = insert.execute()
            Logger.info(f"Event created: {response.get('id')}")
        except Exception as e:
            Logger.error(f"Failed to create event: {e}")
            raise

    async def insert_all(self, schedule: Schedule):
        tasks = [self.insert(event) for event in schedule.events]
        await asyncio.gather(
            *tasks
        )

    def authenticate(self) -> Credentials:
        creds = None
        token_path = FileHandler.secret_path('token.json')
        cred_path = FileHandler.secret_path('credentials.json')

        if FileHandler.exists(token_path):
            creds = Credentials.from_authorized_user_file(
                token_path, self.scopes
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(self.client.request)
            else:
                flow = InstalledAppFlow.from_client_secrets_file(cred_path, self.scopes)
                creds = flow.run_local_server(port=0)

            FileHandler.write(
                token_path, creds.to_json()
            )

        return creds
