from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse(self, sentence: str):
        pass

    @staticmethod
    def __pattern_match(sentence: str) -> tuple:
        pass
