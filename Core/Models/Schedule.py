from Core.Models.Events.Event import Event
from Core.Models.Time.Recurrence import Recurrence


class Schedule:
    def __init__(self, events: list[Event], schedule_session: Recurrence):
        self.events = events
        self.session = schedule_session