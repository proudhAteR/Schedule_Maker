import asyncio
from datetime import datetime

from Core.Models.Enum.Priority import Priority
from Core.Models.Events.Event import Event
from Core.Models.Schedule import Schedule
from Core.Models.Time.Recurrence import Recurrence
from Infrastructure.Utils.Logs.Logger import Logger
from Infrastructure.Utils.Parser.EventParser import EventParser


class EventService:
    def __init__(self):
        self.parser = EventParser()

    # @PerformanceTracker.timeit()
    async def create_event(self, sentence: str, priority: str | None = None,
                           recurrence: Recurrence | None = None) -> Event:

        try:
            event = await self.parser.parse(sentence, recurrence)

            if priority:
                event.priority = Priority.from_str(priority)

            return event
        except ValueError as e:
            Logger.error(f"Unable to create event. Cause: {e}")
            raise

    async def create_schedule(self, block: list[str], date_str: str | None = None) -> Schedule:
        recurrence = None

        if date_str:
            recurrence = Recurrence(
                first_occurrence=datetime.strptime(date_str, "%Y-%m-%d")
            )

        async def parse_line(line: str):
            try:
                return await self.create_event(line, recurrence=recurrence)
            except Exception as e:
                Logger().error(f"Failed to parse line: '{line}'. Reason: {e}")
                return None

        tasks = [parse_line(line) for line in block]
        results = await asyncio.gather(*tasks)

        events = [e for e in results if e is not None]

        return Schedule(events, recurrence)
