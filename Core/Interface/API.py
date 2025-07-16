from abc import ABC, abstractmethod

from Core.Models.Events.Event import Event
from Core.Models.Schedule import Schedule


class API(ABC):
    @abstractmethod
    async def insert(self, event: Event):
        pass

    @abstractmethod
    async def insert_all(self, schedule: Schedule):
        pass

    @abstractmethod
    def authenticate(self):
        pass
