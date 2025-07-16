from abc import ABC, abstractmethod

from Core.Models.Recurrence import Recurrence


class Parser(ABC):
    @abstractmethod
    def parse(self, sentence: str):
        pass

    @classmethod
    def __pattern_match(cls, sentence: str) -> tuple:
        pass