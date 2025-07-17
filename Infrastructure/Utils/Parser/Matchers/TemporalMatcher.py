import calendar
import re
from datetime import datetime, timedelta
import dateparser
from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field


# Used chatgpt a lot here :3
class TemporalMatcher(Matcher):
    def match(self, sentence: str) -> dict[Field, datetime | str]:
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
        if day_str:
            return self.__resolve_with_day(day_str, start_raw, end_raw)

        start = self.__parse_or_now(start_raw)
        end = self.__parse_or_now(end_raw)
        return start, end

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
            # from X to Y, between X and Y
            r"(?:from|between)\s+(?P<start>\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\s+(?:to|and)\s+(?P<end>\d{1,2}(?::\d{2})?\s*(?:am|pm)?)",
            # X to Y am/pm or X-Y am/pm
            r"\b(\d{1,2}(?::\d{2})?)\s*(?:-|to|and)\s*(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
            # X am to Y pm (different meridiem)
            r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\s+(?:to|and)\s+(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                if 'start' in match.groupdict() and 'end' in match.groupdict():
                    start_raw = match.group('start').strip()
                    end_raw = match.group('end').strip()
                elif len(match.groups()) == 3:
                    start_raw = f"{match.group(1)} {match.group(3)}"
                    end_raw = f"{match.group(2)} {match.group(3)}"
                elif len(match.groups()) == 4:
                    start_raw = f"{match.group(1)} {match.group(2)}"
                    end_raw = f"{match.group(3)} {match.group(4)}"
                else:
                    continue
                return cls.__normalize_time_pair(start_raw, end_raw)

        # Find any two times with am/pm
        time_pattern = r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\b"
        times = re.findall(time_pattern, sentence, re.IGNORECASE)
        if len(times) >= 2:
            start_raw = f"{times[0][0]} {times[0][1]}"
            end_raw = f"{times[1][0]} {times[1][1]}"
            return cls.__normalize_time_pair(start_raw, end_raw)

        # Fallback
        raw_times = re.findall(r"\b\d{1,2}(?::\d{2})?\s*(?:am|pm)?\b", sentence, re.IGNORECASE)
        if len(raw_times) >= 2:
            return cls.__normalize_time_pair(raw_times[0], raw_times[1])

        return None, None

    @staticmethod
    def __normalize_time_pair(start_raw: str, end_raw: str) -> tuple[str, str]:
        start_raw = start_raw.strip()
        end_raw = end_raw.strip()

        def add_meridiem_if_missing(time_str: str, default_meridiem: str) -> str:
            if not re.search(r"\b(am|pm)\b", time_str, re.IGNORECASE):
                return f"{time_str} {default_meridiem}"
            return time_str

        # Use meridiem from end if missing in start
        if not re.search(r"\b(am|pm)\b", start_raw, re.IGNORECASE):
            meridiem_match = re.search(r"\b(am|pm)\b", end_raw, re.IGNORECASE)
            if meridiem_match:
                start_raw = add_meridiem_if_missing(start_raw, meridiem_match.group(1))

        # Default to am or pm based on hour if still missing
        if not re.search(r"\b(am|pm)\b", start_raw, re.IGNORECASE):
            hour = int(re.match(r"\d{1,2}", start_raw).group())
            start_raw = add_meridiem_if_missing(start_raw, "am" if hour < 12 else "pm")

        if not re.search(r"\b(am|pm)\b", end_raw, re.IGNORECASE):
            hour = int(re.match(r"\d{1,2}", end_raw).group())
            end_raw = add_meridiem_if_missing(end_raw, "am" if hour < 12 else "pm")

        return start_raw, end_raw

    @staticmethod
    def __resolve_with_day(day_name: str, start_raw: str, end_raw: str) -> tuple[datetime, datetime]:
        base_date = TemporalMatcher.__get_next_weekday(day_name)

        start_time = dateparser.parse(start_raw)
        end_time = dateparser.parse(end_raw)

        if start_time is None or end_time is None:
            return base_date, base_date

        start = base_date.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
        end = base_date.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)

        if end <= start:
            end += timedelta(days=1)

        return start, end

    @staticmethod
    def __get_next_weekday(day_name: str) -> datetime:
        today = datetime.now()
        target_index = list(calendar.day_name).index(day_name)
        days_ahead = (target_index - today.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)
