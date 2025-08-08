import re
from asyncio import gather

from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field
from Infrastructure.Utils.Parser.Matchers.Temporal.Extractors.DayExtractor import DayExtractor
from Infrastructure.Utils.Parser.Matchers.Temporal.Extractors.TimeExtractor import TimeExtractor
from Infrastructure.Utils.Parser.Matchers.Temporal.FallbackHandler import FallbackHandler
from Infrastructure.Utils.Parser.Matchers.Temporal.TimeResolver import TimeResolver


class TemporalMatcher(Matcher):
    def __init__(self):
        self.time_pattern = re.compile(r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\b", re.IGNORECASE)
        self.day_extractor = DayExtractor()
        self.time_extractor = TimeExtractor(self.time_pattern)
        self.fallback_handler = FallbackHandler(self.time_pattern)
        self.resolver = TimeResolver()

        super().__init__()

    async def match(self, tokens: dict) -> dict:
        sentence = tokens.get('time', '').strip()
        if not sentence:
            raise ValueError("No sentence detected.")

        day_str, is_recurring, start_raw, end_raw = await self.__extract_components(sentence)

        if not start_raw or not end_raw:
            return self.fallback_handler.handle(sentence, day_str)

        start, end = self.resolver.run(day_str, start_raw, end_raw)

        return {
            Field.DAY: day_str if is_recurring else '',
            Field.START: start,
            Field.END: end
        }

    async def __extract_components(self, sentence: str) -> tuple:
        day_task = self.day_extractor.extract(sentence)
        time_task = self.time_extractor.extract(sentence)

        (day_str, is_recurring), (start_raw, end_raw) = await gather(day_task, time_task)
        return day_str, is_recurring, start_raw, end_raw
