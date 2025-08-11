from typing import Generic, TypeVar

from Core.Interface.APIs.CalendarAPI import CalendarAPI
from Infrastructure.Services.EventService import EventService
from Infrastructure.Services.Google.GoogleCalendar import GoogleCalendar

TCalendar = TypeVar("TCalendar", bound=CalendarAPI)


class Schedule_Maker(Generic[TCalendar]):
    def __init__(self, calendar: TCalendar | None = None):
        self.calendar = calendar or GoogleCalendar()
        self.service = EventService()

    async def event(self, sentence: str, priority: str):
        e = await self.service.create_event(sentence, priority)
        await self.calendar.insert(e)

    async def schedule(self, block: list[str], date: str | None = None):
        s = await self.service.create_schedule(block, date)
        await self.calendar.insert_all(s)

    async def overview(self, date_str: str | None):
        date = await self.service.overview_date(date_str)
        await self.calendar.get_schedule(date)
