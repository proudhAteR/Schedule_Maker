from datetime import datetime, timedelta, time

import dateparser

from Infrastructure.Utils.Parser.Matchers.Temporal.FallbackHandler import FallbackHandler
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class TimeResolver:

    def __init__(self):
        self.parser = TimeParser()

    def run(self, day_str: str, start_raw: str, end_raw: str) -> tuple:
        base_date = self._resolve_day_expression(day_str)
        start_time, end_time = self._parse_time_period(start_raw, end_raw)

        if not start_time or not end_time:
            return base_date, base_date

        return self._resolve_datetime_range(base_date, start_time, end_time)

    def _parse_time_period(self, start_raw: str, end_raw: str) -> tuple:
        start_time = self.parser.parse(start_raw)
        end_time = self.parser.parse(end_raw)

        if start_time == end_time:
            end_time = FallbackHandler.next_hour(end_time)

        return start_time, end_time

    @staticmethod
    def _resolve_day_expression(day_str: str | None) -> datetime:
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if not day_str or not day_str.strip():
            return today

        parsed_date = dateparser.parse(day_str.strip())
        return parsed_date.replace(hour=0, minute=0, second=0, microsecond=0) if parsed_date else today

    @staticmethod
    def _resolve_datetime_range(base_date: datetime, start_time: time, end_time: time) -> tuple:
        now = datetime.now()
        start_dt = datetime.combine(base_date.date(), start_time)
        end_dt = datetime.combine(base_date.date(), end_time)

        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        if base_date.date() == now.date() and start_dt <= now:
            start_dt += timedelta(days=7)
            end_dt += timedelta(days=7)

        return start_dt, end_dt
