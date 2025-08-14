import re
from datetime import time, datetime, timedelta

import dateparser

from Core.Interface.Parser import Parser
from Infrastructure.Utils.Helpers.Patterns.Regex.patterns import RE_HOUR_ONLY, RE_12H, RE_24H


class TimeParser(Parser):
    _DATEPARSER_SETTINGS = {"RETURN_AS_TIMEZONE_AWARE": True}
    _ONE_DAY = timedelta(days=1)

    def parse(self, time_str: str):
        if not time_str or not time_str.strip():
            return None

        time_str = time_str.strip()

        # 1. Try dateparser
        parsed = dateparser.parse(time_str)
        if parsed:
            if parsed.time() == time(0, 0) and RE_HOUR_ONLY.fullmatch(time_str):
                return self._parse_hour_only(time_str)
            return parsed.time()

        # 2. Try 24-hour format
        if RE_24H.fullmatch(time_str):
            return self._parse_24h(time_str)

        # 3. Try 12-hour format
        match = RE_12H.fullmatch(time_str)
        if match:
            return self._parse_12h(match)

        return None

    @staticmethod
    def _parse_hour_only(hour_str: str):
        hour = int(hour_str)
        return time(hour, 0) if 0 <= hour <= 23 else None

    @staticmethod
    def _parse_24h(time_str: str):
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            return None

    @staticmethod
    def _parse_12h(match: re.Match):
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        meridiem = match.group(3).lower()

        if meridiem == "pm" and hour != 12:
            hour += 12
        elif meridiem == "am" and hour == 12:
            hour = 0

        return time(hour, minute)

    @staticmethod
    def pattern(match: re.Match, pattern_index: int) -> tuple:
        groups = match.groups()
        patterns = {
            0: lambda g: (g[0].strip(), g[1].strip()),
            5: lambda g: (g[0].strip(), g[1].strip()),
            1: lambda g: (f"{g[0]} {g[1]}", f"{g[2]} {g[3]}"),
            2: lambda g: (f"{g[0]} {g[2]}", f"{g[1]} {g[2]}"),
            3: lambda g: (f"{g[0]}:{g[1]}", f"{g[2]}:{g[3]}"),
            4: lambda g: (f"{g[0]}:00", f"{g[1]}:00"),
            6: lambda g: (f"{g[0]} {g[1]}", f"{g[0]} {g[1]}")
        }
        return patterns.get(pattern_index, lambda g: ("", ""))(groups)

    # noinspection PyTypeChecker
    @classmethod
    def get_date(cls, date_str: str | None):
        dt = dateparser.parse(date_str, settings=cls._DATEPARSER_SETTINGS) if date_str else None
        return dt or datetime.now().astimezone()

    @staticmethod
    def midnight(date: datetime) -> datetime:
        return date.replace(hour=0, minute=0, second=0, microsecond=0)

    @classmethod
    def get_possible_time_range(cls, date: datetime):
        time_min = date.isoformat()
        time_max = (date + cls._ONE_DAY).isoformat()
        return time_min, time_max

    @staticmethod
    async def convert_time(event_data: dict) -> str:
        start_raw = event_data.get("start", {}).get("dateTime") or event_data.get("start", {}).get("date")

        if start_raw.endswith("Z"):
            start_raw = start_raw.replace("Z", "+00:00")

        start_dt = datetime.fromisoformat(start_raw)
        return start_dt.strftime("%I:%M %p")
