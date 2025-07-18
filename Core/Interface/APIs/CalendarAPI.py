from abc import abstractmethod

from Core.Interface.APIs.API import API
from Core.Models.Events.Event import Event
from Core.Models.Schedule import Schedule


class CalendarAPI(API):
    def __init__(self):
        pass

    @abstractmethod
    async def insert(self, event: Event):
        pass

    @abstractmethod
    async def insert_all(self, schedule: Schedule):
        pass
