from datetime import datetime

from Core.Models.Events.Event import Event
from Core.Models.Recurrence import Recurrence
from Infrastructure.Services.EventService import EventService
from Infrastructure.Utils.Logger import Logger


class Schedule:
    def __init__(self, events: list[Event], schedule_session: Recurrence):
        self.events = events
        self.session = schedule_session