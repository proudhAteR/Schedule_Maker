from abc import abstractmethod

from Core.Interface.APIs.API import API


class TranslationAPI(API):
    @staticmethod
    @abstractmethod
    def detect_lang(text: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def translate(text: str, to_lang: str = 'en') -> str:
        pass
