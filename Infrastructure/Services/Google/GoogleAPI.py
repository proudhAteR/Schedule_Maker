from asyncio import gather

from google.auth.exceptions import TransportError
from googleapiclient.discovery import build
from Core.Interface.API import API
from Core.Models.Events.Event import Event
from Core.Models.Schedule import Schedule
from Infrastructure.Clients.GoogleClient import GoogleClient
from Infrastructure.Services.Google.GoogleAuth import GoogleAuth
from Infrastructure.Utils.Logs.Logger import Logger


class GoogleAPI(API):
    def __init__(self):
        try:
            self.client = GoogleClient('calendar')
            self.authenticator = GoogleAuth(self.client)
            self.creds = self.authenticator.auth()
            self.resource = build(self.client.service, 'v3', credentials=self.creds)
        except (TransportError, FileNotFoundError) as e:
            Logger.error(f"Error while trying to authenticate : {e}")

    async def insert(self, event: Event, calendar_id: str = 'primary'):
        try:
            events = self.resource.events()
            insert = events.insert(
                calendarId=calendar_id, body=event.to_google_event()
            )
            response = insert.execute()
            Logger.info(f"Event created: {response.get('id')}")
        except Exception as e:
            Logger.error(f"Failed to create event: {e}")
            raise

    async def insert_all(self, schedule: Schedule):
        tasks = [
            self.insert(event) for event in schedule.events
        ]
        await gather(*tasks)
