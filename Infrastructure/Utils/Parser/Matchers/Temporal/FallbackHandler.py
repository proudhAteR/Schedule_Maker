import re
from datetime import datetime, timedelta, time

import dateparser

from Core.Models.Enum.Field import Field
from Infrastructure.Utils.Parser.Matchers.Temporal.Extractors.DayExtractor import DayExtractor
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class FallbackHandler:
    def __init__(self, expressions: dict, pattern: re.Pattern):
        self.time_only_pattern = pattern
        self.parser = TimeParser()
        self.expressions = expressions
        self.day = DayExtractor()

    def handle(self, sentence: str, day_str: str) -> dict:
        """Handle fallback cases when time extraction fails."""
        fallback_time = self._extract_any_time(sentence)
        fallback_date = dateparser.parse(day_str)

        fallback_time = self.__get_fallback(fallback_date, fallback_time)

        return {
            Field.DAY: day_str,
            Field.START: fallback_time,
            Field.END: self.next_hour(fallback_time),
        }

    @staticmethod
    def __get_fallback(fallback_date, fallback_time):
        if not fallback_date:
            fallback_date = datetime.now()
        if isinstance(fallback_time, time):
            fallback_time = datetime.combine(fallback_date.date(), fallback_time)
        elif not isinstance(fallback_time, datetime):
            fallback_time = fallback_date

        return fallback_time

    @staticmethod
    def next_hour(given: time) -> time:
        dummy_dt = datetime.combine(datetime.today(), given)
        incremented = dummy_dt + timedelta(hours=1)
        return incremented.time()

    def _extract_any_time(self, sentence: str) -> datetime | None:
        """Extract any time information as fallback."""
        times = self.time_only_pattern.findall(sentence)
        if times:
            time_str = f"{times[0][0]} {times[0][1]}"
            return self.parser.parse(time_str)

        for expr, replacement in self.expressions.items():
            if expr in sentence.lower():
                return self.parser.parse(replacement)

        return None
