from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from Clients.Client import Client
from Models.Event import Event
from Models.Schedule import Schedule
from Utils.FileHandler import FileHandler
from Utils.Logger import Logger

logger = Logger().logger

class APIService:
    def __init__(self):
        self.client = Client('https://www.googleapis.com/auth/calendar')
        self.scopes = [self.client.base_url]
        self.creds = self.authenticate()
        self.res = build('calendar', 'v3', credentials=self.creds)

    def create_event(self, event: Event, calendar_id: str = 'primary'):
        try:
            events = self.res.events()
            insert = events.insert(calendarId=calendar_id, body=event.to_google_event())
            response = insert.execute()
            logger.info(f"Event created: {response.get('id')}")
        except Exception as e:
            logger.error(f"Failed to create event: {e}")
            raise

    def make_schedule(self, schedule: Schedule):
        for event in schedule.events:
            self.create_event(event)

    def authenticate(self) -> Credentials:
        creds = None

        if FileHandler.exists("secrets/token.json"):
            creds = Credentials.from_authorized_user_file("secrets/token.json", self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'secrets/credentials.json', self.scopes
                )
                creds = flow.run_local_server(port=0)

            FileHandler.write('secrets/token.json', creds.to_json())

        return creds
