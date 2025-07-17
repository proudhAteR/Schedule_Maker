from typing import Generic, TypeVar

from Core.Interface.APIs.CalendarAPI import CalendarAPI
from Infrastructure.Services.EventService import EventService
from Infrastructure.Utils.Logs.Logger import Logger

TCalendar = TypeVar("TCalendar", bound=CalendarAPI)


class Schedule_Maker(Generic[TCalendar]):
    def __init__(self, calendar: TCalendar):
        self.calendar = calendar
        self.service = EventService()

    async def event(self, sentence: str, priority: str):
        try:
            event = self.service.create_event(sentence, priority)
            await self.calendar.insert(event)
        except ValueError as e:
            Logger.error(f"Unable to create event. Cause: {e}")

    async def schedule(self, block: list[str], date: str | None = None):
        try:
            schedule = self.service.create_schedule(block, date)
            await self.calendar.insert_all(schedule)
        except ValueError as e:
            Logger.error(f"Unable to create schedule. Cause: {e}")
