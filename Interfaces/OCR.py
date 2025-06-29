from abc import ABC, abstractmethod
from numpy import ndarray

from Models.Tables.Box import Box


class OCR(ABC):

    def __init__(self):
        self.config = None
        self.lang = None
        self.debug = False

    @abstractmethod
    def init(self, lang: str = None, debug: bool = False, config: str = None) -> "OCR":
        pass

    def extract(self, src: Box, bit: ndarray, conf_min: int) -> str:
        pass
