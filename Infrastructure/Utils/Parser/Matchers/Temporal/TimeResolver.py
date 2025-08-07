from datetime import datetime, timedelta, time

import dateparser

from Infrastructure.Utils.Parser.Matchers.Temporal.FallbackHandler import FallbackHandler
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class TimeResolver:

    def __init__(self):
        self.parser = TimeParser()

    def run(self, day_str: str, start_raw: str, end_raw: str) -> tuple:
        base_date = self._resolve_day_expression(day_str)
        start_time, end_time = self.__get_period(end_raw, start_raw)

        if not start_time or not end_time:
            return base_date, base_date

        return self.__adapt_time(base_date, end_time, start_time)

    @staticmethod
    def __adapt_time(base_date: datetime, end_time: time, start_time: time):
        start = datetime.combine(base_date.date(), start_time)
        end = datetime.combine(base_date.date(), end_time)

        # Handle overnight periods (e.g., 10 PM – 2 AM)
        if end <= start:
            end += timedelta(days=1)

        return start, end

    def __get_period(self, end_raw: str, start_raw: str) -> tuple:
        start_time = self.parser.parse(start_raw)
        end_time = self.parser.parse(end_raw)

        if start_time == end_time:
            end_time = FallbackHandler.next_hour(end_time)

        return start_time, end_time

    @staticmethod
    def _resolve_day_expression(day_str: str | None) -> datetime:
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if not day_str or not day_str.strip():
            return base_time

        parsed = dateparser.parse(day_str.strip(), settings={"PREFER_DATES_FROM": "future"})

        if parsed:
            return parsed.replace(hour=0, minute=0, second=0, microsecond=0)

        return base_time
