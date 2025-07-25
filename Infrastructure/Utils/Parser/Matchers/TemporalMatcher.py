import re
from asyncio import gather

from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field
from Infrastructure.Utils.Parser.Matchers.Temporal.Extractors.DayExtractor import DayExtractor
from Infrastructure.Utils.Parser.Matchers.Temporal.Extractors.TimeExtractor import TimeExtractor
from Infrastructure.Utils.Parser.Matchers.Temporal.FallbackHandler import FallbackHandler
from Infrastructure.Utils.Parser.Matchers.Temporal.Normalizer import Normalizer
from Infrastructure.Utils.Parser.Matchers.Temporal.TimeResolver import TimeResolver

# Used claude and Chatgpt for the logic :3

TIME_EXPRESSIONS = {
    'noon': '12:00 pm',
    'midnight': '12:00 am',
    'morning': '9:00 am',
    'afternoon': '2:00 pm',
    'evening': '6:00 pm',
    'night': '9:00 pm'
}


class TemporalMatcher(Matcher):
    def __init__(self):
        self.time_only_pattern = re.compile(r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\b", re.IGNORECASE)
        self.day_extract = DayExtractor()
        self.time_extract = TimeExtractor(
            TIME_EXPRESSIONS,
            self.time_only_pattern
        )
        self.fallback = FallbackHandler(TIME_EXPRESSIONS, self.time_only_pattern)
        self.resolver = TimeResolver()
        self.normalizer = Normalizer(TIME_EXPRESSIONS)
        super().__init__()

    async def match(self, tokens: dict) -> dict:
        sentence = tokens.get('time', '')
        if not sentence or not sentence.strip():
            raise ValueError("No sentence detected.")

        day_str, start_raw, end_raw = await self.__extract_time(sentence)

        if not start_raw or not end_raw:
            return self.fallback.handle(sentence, day_str)

        start, end = self.resolver.run(day_str, start_raw, end_raw)

        return {
            Field.DAY: day_str,
            Field.START: start,
            Field.END: end
        }

    async def __extract_time(self, sentence: str):
        normalized = self.normalizer.run(sentence)

        day_str_task = self.day_extract.extract(normalized)
        time_task = self.time_extract.extract(normalized)

        day_str, (start_raw, end_raw) = await gather(
            day_str_task,
            time_task
        )

        return day_str, start_raw, end_raw