import asyncio
from datetime import datetime

from Core.Interface.APIs.TranslationAPI import TranslationAPI
from Core.Interface.Matcher import Matcher
from Core.Interface.Tokenizer import Tokenizer
from Core.Models.Match import Match
from Infrastructure.Services.Google.GoogleTranslator import GoogleTranslator
from Infrastructure.Services.Language.Spacy import Spacy
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class LanguageService:
    def __init__(self, translator: TranslationAPI = GoogleTranslator(), tokenizer: Tokenizer = Spacy()):
        self._translator = translator
        self._tokenizer = tokenizer
        self._matchers = [matcher() for matcher in Matcher.all_subclasses()]

    async def process(self, sentence: str) -> dict:
        if not sentence:
            return {}

        translated = await self._translator.translate_async(sentence.strip())
        return self._tokenizer.tokenize(translated)

    async def match(self, sentence: str) -> Match:
        tokens = await self.process(sentence)
        match_results = await asyncio.gather(*[matcher.match(tokens) for matcher in self._matchers])
        aggr = self._aggregate_matches(match_results)

        return Match.from_data(aggr)

    @staticmethod
    def _aggregate_matches(results: list) -> dict:
        data = {}
        for res in results:
            if isinstance(res, dict):
                data.update(res)
        return data

    async def parse_datetime(self, date_str: str | None) -> datetime:
        tokens = await self.process(date_str or '')
        time = tokens.get("time", '')

        return TimeParser.get_date(time)
