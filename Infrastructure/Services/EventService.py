from datetime import datetime

from Core.Models.Enum.Priority import Priority
from Core.Models.Events.Event import Event
from Core.Models.Recurrence import Recurrence
from Core.Models.Schedule import Schedule
from Infrastructure.Utils.EventParser import EventParser
from Infrastructure.Utils.Logger import Logger


class EventService:
    def __init__(self):
        self.parser = EventParser()

    def create_event(self, sentence: str, priority: str = "casual", recurrence: Recurrence | None = None) -> Event:
        event: Event = self.parser.parse(sentence, recurrence)
        event.priority = Priority.from_str(priority)

        return event

    def create_schedule(self, block: list[str], date_str: str | None = None) -> Schedule:
        events = []
        recurrence = None
        if date_str:
            recurrence = Recurrence(
                first_occurrence=datetime.strptime(date_str, "%Y-%m-%d")
            )

        for line in block:
            try:
                event = self.create_event(line, recurrence=recurrence)
                events.append(event)
            except Exception as e:
                Logger().error(f"Failed to parse line: '{line}'. Reason: {e}")

        return Schedule(events, recurrence)
