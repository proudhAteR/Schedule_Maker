import calendar
import re
from datetime import datetime, timedelta
import dateparser
from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field


# Used chatgpt a lot here :3
class TemporalMatcher(Matcher):
    def __init__(self):
        super().__init__()

    async def match(self, sentence: str) -> dict[Field, datetime | str]:
        day_str = self.__extract_day(sentence)
        start_raw, end_raw = self.__extract_time_range(sentence)

        if not start_raw or not end_raw:
            fallback = self.__parse_or_now(sentence)
            return {
                Field.DAY: day_str,
                Field.START: fallback,
                Field.END: fallback,
            }

        start, end = self.resolve_time_range(day_str, end_raw, start_raw)

        return {
            Field.DAY: day_str,
            Field.START: start,
            Field.END: end
        }

    def resolve_time_range(self, day_str: str, end_raw: str, start_raw: str) -> tuple:
        base_date = self.__get_next_weekday(day_str)
        start_time, end_time = self.__get_period(start_raw, end_raw)

        if start_time is None or end_time is None:
            return base_date, base_date

        start = base_date.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
        end = base_date.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)

        if end <= start:
            end += timedelta(days=1)

        return start, end

    def __get_period(self, end_raw, start_raw):
        start = self.__parse_or_now(start_raw)
        end = self.__parse_or_now(end_raw)
        return end, start

    @staticmethod
    def __parse_or_now(time_str: str) -> datetime:
        dt = dateparser.parse(time_str)
        return dt if dt else datetime.now()

    @staticmethod
    def __extract_day(sentence: str) -> str:
        pattern = (
            r"\b(?:every|on|this|next)?\s*"
            r"(mon(?:day)?|tue(?:sday)?|tues|wed(?:nesday)?|weds|thu(?:rsday)?|thurs|fri(?:day)?|"
            r"sat(?:urday)?|sun(?:day)?)s?\b"
        )
        match = re.search(pattern, sentence, re.IGNORECASE)
        if not match:
            return ""

        short_day = match.group(1)[:3].lower()
        return next((day for day in calendar.day_name if day.lower().startswith(short_day)), "")

    @classmethod
    def __extract_time_range(cls, sentence: str) -> tuple[str | None, str | None]:
        patterns = [
            # 1. X am to Y pm
            r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\s+(?:to|and)\s+(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",

            # 2. X to Y am/pm (e.g. 4 to 5 pm)
            r"\b([1-9]|1[0-2])(?::\d{2})?\s*(?:\-|–|—|to|and)\s*([1-9]|1[0-2])(?::\d{2})?\s*(am|pm)\b",

            # 3. Named groups (fallback — handles both 12 and 24-hour with or without am/pm)
            r"(?:from|between)\s+(?P<start>\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\s+(?:to|and)\s+(?P<end>\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)",

            # 4. 24-hour format (last resort)
            r"\b([01]?\d|2[0-3])(?::\d{2})?\s*(?:\-|–|—|to|and)\s*([01]?\d|2[0-3])(?::\d{2})?\b",
        ]

        for pattern in patterns:
            sentence = re.sub(r"\.", "", sentence)
            match = re.search(pattern, sentence, re.IGNORECASE)
            if not match:
                continue

            if 'start' in match.groupdict() and 'end' in match.groupdict():
                start = match.group('start').strip()
                end = match.group('end').strip()
                start_mer = match.group('start_meridiem') or match.group('end_meridiem')  # fallback
                end_mer = match.group('end_meridiem') or start_mer

                start_raw = f"{start} {start_mer}".strip()
                end_raw = f"{end} {end_mer}".strip()
            elif len(match.groups()) == 3:
                # This pattern captures e.g. '4 to 5 pm' (meridiem only present once)
                hour1, hour2, meridiem = match.groups()
                meridiem = meridiem.strip().lower()
                start_raw = f"{hour1.strip()} {meridiem}"
                end_raw = f"{hour2.strip()} {meridiem}"

            elif len(match.groups()) == 4:

                # e.g. 4 am to 5 pm
                start_raw = f"{match.group(1).strip()} {match.group(2).strip()}"
                end_raw = f"{match.group(3).strip()} {match.group(4).strip()}"
            elif len(match.groups()) == 2:

                # 24-hour times, no am/pm
                start_raw = match.group(1).strip()
                end_raw = match.group(2).strip()

            else:
                continue

            return cls.__normalize_time_pair(start_raw, end_raw)

        # fallback with am/pm times
        time_pattern = r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\b"
        times = re.findall(time_pattern, sentence, re.IGNORECASE)
        if len(times) >= 2:
            start_raw = f"{times[0][0]} {times[0][1]}"
            end_raw = f"{times[1][0]} {times[1][1]}"
            return cls.__normalize_time_pair(start_raw, end_raw)

        # fallback without am/pm
        raw_times = re.findall(r"\b\d{1,2}(?::\d{2})?\b", sentence, re.IGNORECASE)
        if len(raw_times) >= 2:
            return cls.__normalize_time_pair(raw_times[0], raw_times[1])

        return None, None

    @staticmethod
    def __normalize_time_pair(start_raw: str, end_raw: str) -> tuple[str, str]:
        start_raw = start_raw.strip()
        end_raw = end_raw.strip()

        def is_24_hour_format(time_str: str) -> bool:
            match = re.match(r"^([01]?\d|2[0-3])(?::\d{2})?$", time_str)
            return bool(match)

        def add_meridiem_if_missing(time_str: str, default_meridiem: str) -> str:
            if re.search(r"\b(am|pm)\b", time_str, re.IGNORECASE) or is_24_hour_format(time_str):
                return time_str  # Don't touch it
            return f"{time_str} {default_meridiem}"

        # Use meridiem from end if missing in start
        if not re.search(r"\b(am|pm)\b", start_raw, re.IGNORECASE) and not is_24_hour_format(start_raw):
            meridiem_match = re.search(r"\b(am|pm)\b", end_raw, re.IGNORECASE)
            if meridiem_match:
                start_raw = add_meridiem_if_missing(start_raw, meridiem_match.group(1))

        # Default to am/pm only if both are still unclear
        if not re.search(r"\b(am|pm)\b", start_raw, re.IGNORECASE) and not is_24_hour_format(start_raw):
            hour = int(re.match(r"\d{1,2}", start_raw).group())
            start_raw = add_meridiem_if_missing(start_raw, "am" if hour < 12 else "pm")

        if not re.search(r"\b(am|pm)\b", end_raw, re.IGNORECASE) and not is_24_hour_format(end_raw):
            hour = int(re.match(r"\d{1,2}", end_raw).group())
            end_raw = add_meridiem_if_missing(end_raw, "am" if hour < 12 else "pm")

        return start_raw, end_raw

    @staticmethod
    def __get_next_weekday(day_name: str | None) -> datetime:
        if not day_name or not day_name.strip():
            return datetime.now()  # Return today if no day name provided

        today = datetime.now()
        target_index = list(calendar.day_name).index(day_name.capitalize())
        days_ahead = (target_index - today.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7  # get the *next* occurrence, not today
        return today + timedelta(days=days_ahead)
