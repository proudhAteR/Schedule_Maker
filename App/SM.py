from datetime import datetime
from typing import Generic, TypeVar

from Core.Interface.APIs.CalendarAPI import CalendarAPI
from Infrastructure.Services.EventService import EventService
from Infrastructure.Utils.Parsers.TimeParser import TimeParser

TCalendar = TypeVar("TCalendar", bound=CalendarAPI)


class SM(Generic[TCalendar]):
    @classmethod
    async def create(cls, calendar: TCalendar | None = None):
        service = await EventService.create()
        return cls(calendar, service)

    def __init__(self, calendar: TCalendar | None, service: EventService):
        self._calendar = calendar
        self.service = service

    @property
    def calendar(self) -> TCalendar:
        if self._calendar is None:
            from Infrastructure.Services.Google.GoogleCalendar import GoogleCalendar
            self._calendar = GoogleCalendar()
        return self._calendar

    def connect(self):
        self.calendar.authenticate()

    async def event(self, sentence: str, priority: str):
        event = await self.service.create_event(sentence, priority)
        await self.calendar.insert(event)

    async def schedule(self, block: list[str], date: str | None = None):
        schedule_items = await self.service.create_schedule(block, date)
        await self.calendar.insert_all(schedule_items)

    async def overview(self, date_str: str | None) -> tuple:
        date = await self.service.overview_date(date_str)
        events = await self._get_events_for_date(date)
        return [
            await self.service.get_infos(event)
            for event in events
        ], date

    async def _get_events_for_date(self, date: datetime):
        try:
            return await self.calendar.fetch_schedule(
                TimeParser.get_possible_time_range(date)
            )
        except ValueError as e:
            raise RuntimeError(f"Failed to retrieve events at {date.date()}") from e
