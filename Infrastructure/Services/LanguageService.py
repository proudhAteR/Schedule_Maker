import asyncio
from datetime import datetime

from Core.Interface.APIs.TranslationAPI import TranslationAPI
from Core.Interface.Matcher import Matcher
from Core.Interface.Tokenizer import Tokenizer
from Core.Models.Enum.Field import Field
from Core.Models.LanguageMatch import LanguageMatch
from Infrastructure.Services.Google.GoogleTranslator import GoogleTranslator
from Infrastructure.Services.Spacy import Spacy
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class LanguageService:
    def __init__(self, translator: TranslationAPI = GoogleTranslator(), tokenizer: Tokenizer = Spacy()):
        self.__matchers: list[Matcher] = [
            matcher() for matcher in Matcher.all_subclasses()
        ]
        self.__translator = translator
        self.__tokenizer = tokenizer

    async def pattern_match(self, title: str) -> tuple:
        data, title = await self.match_all(title)

        return LanguageMatch(
            title=data.get(Field.TITLE, ""),
            location=data.get(Field.LOCATION, ""),
            start=data.get(Field.START),
            end=data.get(Field.END),
            day_str=data.get(Field.DAY, ""),
            more=data.get(Field.EXTRA, "")
        ), title

    async def process(self, sentence: str) -> dict:
        if not sentence:
            return {}

        sentence = sentence.strip()
        sentence = self.__translate(sentence)

        return self.__tokenizer.tokenize(sentence)

    def __translate(self, text: str, to_lang: str = 'en'):
        return self.__translator.translate(text, to_lang)

    async def match_all(self, sentence: str) -> tuple:
        data = {}

        tokens = await self.process(sentence)

        tasks = [matcher.match(tokens) for matcher in self.__matchers]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for res in results:
            if isinstance(res, dict):
                data.update(res)

        title = tokens.get('title')

        return data, title

    async def parse(self, date_str: str | None) -> datetime:
        tokens = await self.process(date_str)
        return TimeParser.get_date(
            tokens.get('time', '')
        )
