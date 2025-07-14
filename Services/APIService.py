from google.auth.exceptions import TransportError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from Clients.GoogleClient import GoogleClient
from Models.Event import Event
from Models.Schedule import Schedule
from Utils.FileHandler import FileHandler
from Utils.Logger import Logger
import asyncio


class APIService:
    def __init__(self):
        try:
            self.client = GoogleClient('calendar')
            self.scopes = [self.client.base_url]
            self.creds = self.authenticate()
            self.res = build('calendar', 'v3', credentials=self.creds)
        except TransportError as e:
            Logger.error(f"Error while trying to authenticate : {e}")

    def create_event(self, event: Event, calendar_id: str = 'primary'):
        try:
            events = self.res.events()
            insert = events.insert(calendarId=calendar_id, body=event.to_google_event())
            response = insert.execute()
            Logger.info(f"Event created: {response.get('id')}")
        except Exception as e:
            Logger.error(f"Failed to create event: {e}")
            raise

    async def make_schedule(self, schedule: Schedule):
        tasks = [self.create_event(event) for event in schedule.events]
        await asyncio.gather(
            *tasks
        )

    def authenticate(self) -> Credentials:
        creds = None

        if FileHandler.exists("App/secrets/token.json"):
            creds = Credentials.from_authorized_user_file("App/secrets/token.json", self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'App/secrets/credentials.json', self.scopes
                )
                creds = flow.run_local_server(port=0)

            FileHandler.write('App/secrets/token.json', creds.to_json())

        return creds
