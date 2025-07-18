import asyncio

from Core.Interface.APIs.TranslationAPI import TranslationAPI
from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field
from Core.Models.LanguageMatch import LanguageMatch
from Infrastructure.Services.Google.GoogleTranslator import GoogleTranslator


class LanguageService:
    def __init__(self, translator: TranslationAPI = GoogleTranslator()):
        self.__matchers: list[Matcher] = [
            matcher() for matcher in Matcher.all_subclasses()
        ]
        self.__translator = translator

    async def pattern_match(self, sentence: str) -> tuple:
        data, sentence= await self.match_all(sentence)

        return LanguageMatch(
            name=data.get(Field.NAME, ""),
            location=data.get(Field.LOCATION, ""),
            start=data.get(Field.START),
            end=data.get(Field.END),
            day_str=data.get(Field.DAY, ""),
            more=data.get(Field.EXTRA, "")
        ), sentence

    async def __process(self, sentence : str):
        sentence = sentence.strip()
        lang = self.__detect(sentence)
        if lang != "en":
            sentence = self.__translate(sentence, lang)

        return sentence

    def __detect(self, text: str):
        return self.__translator.detect_lang(text)

    def __translate(self, text: str, from_lang: str, to_lang: str = 'en'):
        return self.__translator.translate(text, from_lang, to_lang)

    async def match_all(self, sentence: str):
        data = {}

        sentence = await self.__process(sentence)
        tasks = [matcher.match(sentence) for matcher in self.__matchers]
        results = await asyncio.gather(*tasks)

        for res in results:
            data.update(res)

        return data, sentence
