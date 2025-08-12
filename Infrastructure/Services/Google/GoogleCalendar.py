from asyncio import gather, to_thread
from datetime import datetime, timedelta

from googleapiclient.http import HttpRequest

from Core.Interface.APIs.CalendarAPI import CalendarAPI
from Core.Models.Events.Event import Event
from Core.Models.Schedule import Schedule
from Infrastructure.Services.Google.GoogleAPI import GoogleAPI
from Infrastructure.Utils.Logs.Logger import Logger


class GoogleCalendar(CalendarAPI, GoogleAPI):
    def __init__(self):
        GoogleAPI.__init__(self, 'calendar')
        self.events = self.resource.events()

    async def insert(self, event: Event, calendar_id: str = 'primary'):
        response = await to_thread(self.insert_request, event, calendar_id)
        Logger.success(f"Event created: {response.get('id')}")

    def insert_request(self, event: Event, calendar_id: str = 'primary'):
        request: HttpRequest = self.events.insert(
            calendarId=calendar_id, body=event.to_google_event()
        )
        return request.execute()

    async def insert_all(self, schedule: Schedule):
        tasks = [self.insert(event) for event in schedule.events]
        await gather(*tasks)

    async def get_schedule(self, date: datetime, calendar_id: str = 'primary'):
        try:
            response = await to_thread(self.schedule_request, date, calendar_id)
            events: list[dict] = response.get('items', [])
            return events
        except Exception as e:
            Logger.error(f"Failed to retrieve events at {date.date()}: {e}")
            raise

    def schedule_request(self, date: datetime, calendar_id: str = 'primary'):
        time_min = date.isoformat()
        time_max = (date + timedelta(days=1)).isoformat()
        request: HttpRequest = self.events.list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        )

        return request.execute()
