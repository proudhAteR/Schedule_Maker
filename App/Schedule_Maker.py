from typing import Generic, TypeVar

from Core.Interface.APIs.CalendarAPI import CalendarAPI
from Infrastructure.Services.EventService import EventService

TCalendar = TypeVar("TCalendar", bound=CalendarAPI)


class Schedule_Maker(Generic[TCalendar]):
    def __init__(self, calendar: TCalendar):
        self.calendar: TCalendar = calendar
        self.service = EventService()

    async def event(self, sentence: str, priority: str):
        event = await self.service.create_event(sentence, priority)
        await self.calendar.insert(event)

    async def schedule(self, block: list[str], date: str | None = None):
        schedule = await self.service.create_schedule(block, date)
        await self.calendar.insert_all(schedule)

    async def overview(self, date_str: str | None):
        date = await self.service.get_date(date_str)
        await self.calendar.get_schedule(date)
