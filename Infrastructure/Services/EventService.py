from asyncio import gather

from Core.Models.Enum.Priority import Priority
from Core.Models.Events.Event import Event
from Core.Models.Schedule import Schedule
from Core.Models.Time.Recurrence import Recurrence
from Infrastructure.Utils.Parsers.EventParser import EventParser


class EventService:
    def __init__(self):
        self.__parser = EventParser()

    async def create_event(self, sentence: str, priority: str | None = None,
                           recurrence: Recurrence | None = None) -> Event:
        event = await self.__parser.parse(sentence, recurrence)
        if priority:
            event.priority = Priority.from_str(priority)

        return event

    async def create_schedule(self, block: list[str], date_str: str | None = None) -> Schedule:
        recurrence = None
        if date_str:
            recurrence = Recurrence(first_occurrence=await self.get_date(date_str))

        tasks = [await self.create_event(line, recurrence=recurrence) for line in block]
        results = await gather(*tasks)
        events = [e for e in results if e is not None]

        return Schedule(events, recurrence)

    async def get_date(self, date_str: str):
        return await self.__parser.get_date(date_str)

    async def overview_date(self, date_str: str):
        return await self.__parser.midnight(date_str)

    @staticmethod
    async def get_infos(event):
        summary = event.get("summary", "No title")
        start_str = await EventParser.convert_time(event)
        return start_str, summary
