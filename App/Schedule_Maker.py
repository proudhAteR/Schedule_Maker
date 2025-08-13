from datetime import datetime
from typing import Generic, TypeVar

from Core.Interface.APIs.CalendarAPI import CalendarAPI
from Infrastructure.Services.EventService import EventService
from Infrastructure.Utils.Logs.Logger import Logger
from Infrastructure.Utils.Parser.TimeParser import TimeParser

TCalendar = TypeVar("TCalendar", bound=CalendarAPI)


class Schedule_Maker(Generic[TCalendar]):
    def __init__(self, calendar: TCalendar | None = None):
        self._calendar = calendar
        self.service = EventService()

    @property
    def calendar(self) -> TCalendar:
        if self._calendar is None:
            from Infrastructure.Services.Google.GoogleCalendar import GoogleCalendar
            self._calendar = GoogleCalendar()
        return self._calendar

    async def event(self, sentence: str, priority: str):
        e = await self.service.create_event(sentence, priority)
        await self.calendar.insert(e)

    async def schedule(self, block: list[str], date: str | None = None):
        s = await self.service.create_schedule(block, date)
        await self.calendar.insert_all(s)

    async def overview(self, date_str: str | None):
        d = await self.service.overview_date(date_str)
        try:
            s = await self.calendar.fetch_schedule(
                TimeParser.get_possible_time_range(d)
            )
            await self.display(d, s)
        except ValueError:
            raise Exception(f"Failed to retrieve events at {d.date()}")

    async def display(self, date: datetime, events: list[dict]):
        Logger.success(f"{len(events)} event(s) found on {date.date()}")
        if not events:
            return

        for event in events:
            start_str, summary = await self.service.get_infos(event)
            Logger.info(f"{start_str}: {summary}")

    def connect(self):
        self.calendar.authenticate()
