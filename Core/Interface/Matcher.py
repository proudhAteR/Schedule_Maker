import inspect
from abc import ABC, abstractmethod
from datetime import datetime

from Core.Models.Enum.Field import Field


class Matcher(ABC):
    @abstractmethod
    async def match(self, sentence: str) -> dict[Field, str | datetime]:
        pass

    @classmethod
    def all_subclasses(cls) -> list[type['Matcher']]:
        def recurse(sub):
            return [sub] + [g for sc in sub.__subclasses__() for g in recurse(sc)]

        return [sub for sub in recurse(cls) if not inspect.isabstract(sub)]
