from asyncio import gather, to_thread

from googleapiclient.http import HttpRequest

from Core.Interface.APIs.CalendarAPI import CalendarAPI
from Core.Models.Events.Event import Event
from Core.Models.Schedule import Schedule
from Infrastructure.Services.Google.GoogleAPI import GoogleAPI
from Infrastructure.Utils.Logs.Logger import Logger


class GoogleCalendar(CalendarAPI, GoogleAPI):
    def __init__(self):
        GoogleAPI.__init__(self, 'calendar')
        self.__events = self._resource.events()

    async def insert(self, event: Event, calendar_id: str = "primary"):
        response = await self.__events_request_async("insert", calendarId=calendar_id, body=event)
        Logger.success(f"Event created: {response.get('id')}")

    async def insert_all(self, schedule: Schedule):
        tasks = [self.insert(event) for event in schedule.events]
        await gather(*tasks)

    async def fetch_schedule(self, time_range: tuple, calendar_id: str = "primary"):
        time_min, time_max = time_range
        try:
            response = await self.__events_request_async(
                "list",
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime"
            )
            return response.get("items", [])
        except Exception:
            raise

    async def __events_request_async(self, method: str, **kwargs):
        if "body" in kwargs and isinstance(kwargs["body"], Event):
            kwargs["body"] = kwargs["body"].to_google_event()

        return await to_thread(self.__events_request, method, **kwargs)

    def __events_request(self, method: str, **kwargs):
        request: HttpRequest = getattr(self.__events, method)(**kwargs)
        return self._make_request(request)

    def reconnect(self):
        self._authenticator.reconnect()
