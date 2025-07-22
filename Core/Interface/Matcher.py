import inspect
from abc import ABC, abstractmethod


class Matcher(ABC):
    @abstractmethod
    async def match(self, tokens: dict) -> dict:
        pass

    @classmethod
    def all_subclasses(cls) -> list[type['Matcher']]:
        def recurse(sub):
            return [sub] + [g for sc in sub.__subclasses__() for g in recurse(sc)]

        return [sub for sub in recurse(cls) if not inspect.isabstract(sub)]
