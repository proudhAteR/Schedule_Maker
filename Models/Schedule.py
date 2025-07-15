from datetime import datetime

from Models.Events.Event import Event
from Models.Recurrence import Recurrence
from Services.EventService import EventService
from Utils.Logger import Logger


class Schedule:
    def __init__(self, events: list[Event], schedule_session: Recurrence):
        self.events = events
        self.session = schedule_session

    @classmethod
    def from_block(cls, block: list[str], date_str: str | None = None) -> 'Schedule':
        events = []
        recurrence = None
        if date_str:
            recurrence = Recurrence(
                first_occurrence=datetime.strptime(date_str, "%Y-%m-%d")
            )

        for line in block:
            try:
                event = EventService.create_event(line, recurrence=recurrence)
                events.append(event)
            except Exception as e:
                Logger().error(f"Failed to parse line: '{line}'. Reason: {e}")

        return Schedule(events, recurrence)
