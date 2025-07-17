from asyncio import gather

from Core.Interface.APIs.CalendarAPI import CalendarAPI
from Core.Models.Events.Event import Event
from Core.Models.Schedule import Schedule
from Infrastructure.Services.Google.GoogleAPI import GoogleAPI
from Infrastructure.Utils.Logs.Logger import Logger


class GoogleCalendarAPI(CalendarAPI, GoogleAPI):
    def __init__(self):
        GoogleAPI.__init__(self, 'calendar')

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
        tasks = [self.insert(event) for event in schedule.events]
        await gather(*tasks)
