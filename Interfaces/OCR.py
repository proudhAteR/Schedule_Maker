from abc import ABC, abstractmethod

from PIL import Image


class OCR(ABC):

    @abstractmethod
    def init(self, lang: str, config: str = None) -> "OCR":
        pass

    def extract(self, image: Image, conf_min: int) -> str:
        pass
