import calendar
from datetime import datetime, timedelta, time

from Infrastructure.Utils.Parser.TimeParser import TimeParser


class TimeResolver:

    def __init__(self):
        self.parser = TimeParser()

    def run(self, day_str: str, start_raw: str, end_raw: str) -> tuple:
        """Resolve time range with better error handling."""
        base_date = self._get_next_weekday(day_str)
        start_time, end_time = self.__get_period(end_raw, start_raw)

        if not start_time or not end_time:
            return base_date, base_date

        return self.__adapt_time(base_date, end_time, start_time)

    @staticmethod
    def __adapt_time(base_date: datetime, end_time: time, start_time: time):
        start = datetime.combine(base_date.date(), start_time)
        end = datetime.combine(base_date.date(), end_time)

        # Handle overnight periods
        if end <= start:
            end += timedelta(days=1)

        return start, end

    def __get_period(self, end_raw: str, start_raw: str) -> tuple:
        start_time = self.parser.parse(start_raw)
        end_time = self.parser.parse(end_raw)

        return start_time, end_time

    @staticmethod
    def _get_next_weekday(day_name: str | None) -> datetime:
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if not day_name or not day_name.strip():
            return base_time

        day_name = day_name.strip().capitalize()

        try:
            target_index = list(calendar.day_name).index(day_name)
            today = datetime.now()
            days_ahead = (target_index - today.weekday() + 7) % 7

            if days_ahead == 0:
                days_ahead = 7  # Get next occurrence

            return base_time + timedelta(days=days_ahead)
        except ValueError:
            return base_time
