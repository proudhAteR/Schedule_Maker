from Core.Interface.APIs.API import API
from abc import abstractmethod


class TranslationAPI(API):
    @staticmethod
    @abstractmethod
    def detect_lang(text: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def translate(text: str, from_lang: str, to_lang: str = 'en') -> str:
        pass
