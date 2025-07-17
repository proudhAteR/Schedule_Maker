from Core.Interface.APIs.CalendarAPI import CalendarAPI
from Infrastructure.Services.EventService import EventService
from Infrastructure.Services.Google.GoogleCalendarAPI import GoogleCalendarAPI
from Infrastructure.Utils.Logs.Logger import Logger


class Schedule_Maker:
    def __init__(self):
        self.api: CalendarAPI = GoogleCalendarAPI()
        self.service = EventService()

    async def event(self, sentence: str, priority: str):
        try:
            event = self.service.create_event(sentence, priority)
            await self.api.insert(event)
        except ValueError as e:
            Logger.error(f"Unable to create event. Cause: {e}")

    async def schedule(self, block: list[str], date: str | None = None):
        try:
            schedule = self.service.create_schedule(block, date)
            await self.api.insert_all(schedule)
        except ValueError as e:
            Logger.error(f"Unable to create schedule. Cause: {e}")
