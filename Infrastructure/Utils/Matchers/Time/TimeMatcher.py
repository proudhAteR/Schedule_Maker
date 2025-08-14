import re
from asyncio import gather

from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field
from ._internal.Extractors.DayExtractor import DayExtractor
from ._internal.Extractors.TimeExtractor import TimeExtractor
from ._internal.FallbackHandler import FallbackHandler
from ._internal.TimeResolver import TimeResolver


class TimeMatcher(Matcher):
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

        date, is_recurring, start_raw, end_raw = await self.__extract_components(sentence)

        if not start_raw or not end_raw:
            return self.fallback_handler.handle(sentence, date)

        start, end = self.resolver.run(date, start_raw, end_raw)

        return {
            Field.DAY: date if is_recurring else '',
            Field.START: start,
            Field.END: end
        }

    async def __extract_components(self, sentence: str) -> tuple:
        day_task = self.day_extractor.extract(sentence)
        time_task = self.time_extractor.extract(sentence)

        (day, is_recurring), (start_raw, end_raw) = await gather(day_task, time_task)
        return day, is_recurring, start_raw, end_raw
