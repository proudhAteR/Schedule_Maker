from Core.Models.Events.Event import Event
from Core.Models.Time.Recurrence import Recurrence


class Schedule:
    def __init__(self, events: list[Event], recurrence: Recurrence):
        self.events = events
        self.recurrence = recurrence

    def __iter__(self):
        return iter(self.events)
