from abc import ABC, abstractmethod

from PIL import Image


class OCR(ABC):

    def __init__(self):
        self.config = None
        self.lang = None
        self.debug = False

    @abstractmethod
    def init(self, lang: str = None, debug: bool = False, config: str = None) -> "OCR":
        pass

    def extract(self, image: Image, conf_min: int) -> str:
        pass
