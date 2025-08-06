import asyncio
from datetime import datetime
from typing import Any

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
        self._translator = translator
        self._tokenizer = tokenizer
        self._matchers: list[Matcher] = [matcher() for matcher in Matcher.all_subclasses()]

    async def process_sentence(self, sentence: str) -> dict[str, Any]:
        if not sentence:
            return {}

        translated = self._translator.translate(sentence.strip())
        return self._tokenizer.tokenize(translated)

    async def match(self, sentence: str) -> LanguageMatch:
        tokenized_data = await self.process_sentence(sentence)
        match_results = await asyncio.gather(
            *[matcher.match(tokenized_data) for matcher in self._matchers],
            return_exceptions=True
        )
        aggr = self._aggregate_matches(match_results)

        return LanguageMatch(
            title=aggr.get(Field.TITLE, ''),
            location=aggr.get(Field.LOCATION, ''),
            start=aggr.get(Field.START),
            end=aggr.get(Field.END),
            day_str=aggr.get(Field.DAY, ''),
            extra=aggr.get(Field.EXTRA, '')
        )

    @staticmethod
    def _aggregate_matches(results: list) -> dict:
        data = {}
        for res in results:
            if isinstance(res, dict):
                data.update(res)
        return data

    async def parse_datetime(self, date_str: str | None) -> datetime:
        tokens = await self.process_sentence(date_str or '')
        return TimeParser.get_date(tokens.get("time", ''))
