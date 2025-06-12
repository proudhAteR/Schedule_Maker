from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from Clients.CalendarClient import CalendarClient


class CalendarService:
    def __init__(self):
        self.client = CalendarClient()
        self.flow = InstalledAppFlow.from_client_secrets_file('cred.json', self.client.scope)
        self.creds = self.flow.run_local_server()
        build('calendar', 'v3', credentials=self.creds)
