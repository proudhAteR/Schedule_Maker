from asyncio import gather
from datetime import datetime, timedelta

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
        insert = self.events.insert(
            calendarId=calendar_id, body=event.to_google_event()
        )
        response = insert.execute()
        Logger.success(f"Event created: {response.get('id')}")

    async def insert_all(self, schedule: Schedule):
        tasks = [self.insert(event) for event in schedule.events]
        await gather(*tasks)

    async def get_schedule(self, date: datetime, calendar_id: str = 'primary'):
        try:
            time_min = date.isoformat()
            time_max = (date + timedelta(days=1)).isoformat()

            request = self.events.list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            )

            response = request.execute()
            events: list[dict] = response.get('items', [])

            await self.display(date, events)

        except Exception as e:
            Logger.error(f"Failed to retrieve events at {date.date()}: {e}")
            raise

    @staticmethod
    async def display(date, events):
        Logger.success(f"{len(events)} event(s) found on {date.date()}")
        if not events:
            return

        for e in events:
            start_raw = e.get("start", {}).get("dateTime") or e.get("start", {}).get("date")
            summary = e.get("summary", "No title")

            # Handle possible 'Z' in ISO string
            if start_raw.endswith("Z"):
                start_raw = start_raw.replace("Z", "+00:00")

            start_dt = datetime.fromisoformat(start_raw)
            start_str = start_dt.strftime("%I:%M %p")

            Logger.info(f"{start_str}: {summary}")
