import asyncio
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

    async def translate_async(self, text: str, to_lang: str = "en") -> str:
        return await asyncio.to_thread(self.translate, text, to_lang)
