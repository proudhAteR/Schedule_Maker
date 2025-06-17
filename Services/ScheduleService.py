from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from Clients.Client import Client
from Models.Event import Event
from Services.Logger import get_logger
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED_PATH = os.path.join(BASE_DIR, 'cred.json')
logger = get_logger()

class ScheduleService:
    def __init__(self):
        self.client = Client('https://www.googleapis.com/auth/calendar')
        self.flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, self.client.scope)
        self.creds = self.flow.run_local_server()
        self.API = build('calendar', 'v3', credentials=self.creds)

    def create_event(self, event: Event, calendar_id: str = 'primary'):
        try:
            events = self.API.events()
            insert = events.insert(calendarId=calendar_id, body=event.to_google_event())
            response = insert.execute()
            logger.info(f"Event created: {response.get('id')}")
            return response
        except Exception as e:
            logger.error(f"Failed to create event: {e}")
            raise