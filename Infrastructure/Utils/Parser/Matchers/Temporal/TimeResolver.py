from datetime import datetime, timedelta, time

import dateparser

from Infrastructure.Utils.Parser.Matchers.Temporal.FallbackHandler import FallbackHandler
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class TimeResolver:

    def __init__(self):
        self.parser = TimeParser()

    def run(self, date: datetime, start_raw: str, end_raw: str) -> tuple:
        start_time, end_time = self._parse_time_period(start_raw, end_raw)

        if not start_time or not end_time:
            return date, date

        return self._resolve_datetime_range(date, start_time, end_time)

    def _parse_time_period(self, start_raw: str, end_raw: str) -> tuple:
        start_time = self.parser.parse(start_raw)
        end_time = self.parser.parse(end_raw)

        if start_time == end_time:
            end_time = FallbackHandler.next_hour(end_time)

        return start_time, end_time

    @staticmethod
    def _resolve_datetime_range(base_date: datetime, start_time: time, end_time: time) -> tuple:
        now = datetime.now()
        start_dt = datetime.combine(base_date.date(), start_time)
        end_dt = datetime.combine(base_date.date(), end_time)

        def is_overnight(start: datetime, end: datetime) -> bool:
            return end <= start

        if is_overnight(start_dt, end_dt):
            end_dt += timedelta(days=1)

        if start_dt <= now < end_dt:
            return start_dt, end_dt

        if start_dt <= now:
            start_dt += timedelta(days=7)
            end_dt += timedelta(days=7)

        return start_dt, end_dt