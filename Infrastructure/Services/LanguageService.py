import asyncio
from datetime import datetime

from Core.Interface.APIs.TranslationAPI import TranslationAPI
from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field
from Core.Models.LanguageMatch import LanguageMatch
from Infrastructure.Services.Google.GoogleTranslator import GoogleTranslator
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class LanguageService:
    def __init__(self, translator: TranslationAPI = GoogleTranslator()):
        self.__matchers: list[Matcher] = [
            matcher() for matcher in Matcher.all_subclasses()
        ]
        self.__translator = translator

    async def pattern_match(self, sentence: str) -> tuple:
        data, sentence = await self.match_all(sentence)

        return LanguageMatch(
            name=data.get(Field.NAME, ""),
            location=data.get(Field.LOCATION, ""),
            start=data.get(Field.START),
            end=data.get(Field.END),
            day_str=data.get(Field.DAY, ""),
            more=data.get(Field.EXTRA, "")
        ), sentence

    async def __process(self, sentence: str):
        if not sentence:
            return ''

        sentence = sentence.strip()
        sentence = self.__translate(sentence)

        return sentence

    def __translate(self, text: str, to_lang: str = 'en'):
        return self.__translator.translate(text, to_lang)

    async def match_all(self, sentence: str):
        data = {}

        sentence = await self.__process(sentence)
        tasks = [matcher.match(sentence) for matcher in self.__matchers]
        results = await asyncio.gather(*tasks)

        for res in results:
            data.update(res)

        return data, sentence

    async def parse(self, date_str: str | None) -> datetime:
        date_str = await self.__process(date_str)
        return TimeParser.get_date(date_str)
