from abc import abstractmethod, ABC

from Core.Interface.APIs.API import API


class TranslationAPI(ABC, API):
    @abstractmethod
    def detect_lang(self):
        pass

    @abstractmethod
    def translate(self):
        pass
