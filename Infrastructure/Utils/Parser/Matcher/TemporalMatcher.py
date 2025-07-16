import calendar
import re
from datetime import datetime, timedelta
import dateparser

from Core.Interface.Matcher import Matcher


class TemporalMatcher(Matcher):

    def match(self, sentence: str) -> tuple[str, datetime, datetime]:
        day_str = self.__extract_day(sentence)
        start_raw, end_raw = self.__extract_time_range(sentence)

        if not start_raw or not end_raw:
            fallback = dateparser.parse(sentence)
            return day_str, fallback, fallback

        if day_str:
            start, end = self.__resolve_with_day(day_str, start_raw, end_raw)
        else:
            start = dateparser.parse(start_raw)
            end = dateparser.parse(end_raw)

        return day_str, start, end

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

    @staticmethod
    def __extract_time_range(sentence: str) -> tuple:
        pattern = (
            r"(?:from|between)\s+"
            r"(?P<start>\d{1,2}(?::\d{2})?)\s+"
            r"(?:to|and)\s+"
            r"(?P<end>\d{1,2}(?::\d{2})?\s*(?:am|pm))"
        )
        match = re.search(pattern, sentence, re.IGNORECASE)
        if match:
            return TemporalMatcher.parse(
                match.group("start"),
                match.group("end")
            )

        # Case: "7 to 8 am" or "7-8 am"
        loose_match = re.search(
            r"\b(\d{1,2})\s*(?:-|to|and)\s*(\d{1,2})\s*(am|pm)\b", sentence, re.IGNORECASE
        )
        if loose_match:
            meridiem = loose_match.group(3)
            return (
                f"{loose_match.group(1)} {meridiem}",
                f"{loose_match.group(2)} {meridiem}"
            )

        raw_times = re.findall(r"\b\d{1,2}(?::\d{2})?\s*(?:am|pm)?", sentence, re.IGNORECASE)
        if len(raw_times) >= 2:
            return raw_times[0], raw_times[1]

        return None, None

    @staticmethod
    def parse(start_raw: str, end_raw: str) -> tuple:
        if not re.search(r"\b(am|pm)\b", start_raw, re.IGNORECASE):
            meridiem_match = re.search(r"\b(am|pm)\b", end_raw, re.IGNORECASE)
            if meridiem_match:
                start_raw = f"{start_raw} {meridiem_match.group(1)}"
        return start_raw.strip(), end_raw.strip()

    @staticmethod
    def __resolve_with_day(day_name: str, start_raw: str, end_raw: str) -> tuple:
        base_date = TemporalMatcher.__get_next_weekday(day_name)

        start_time = dateparser.parse(start_raw)
        end_time = dateparser.parse(end_raw)

        start = base_date.replace(hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
        end = base_date.replace(hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)

        return start, end

    @staticmethod
    def __get_next_weekday(day_name: str) -> datetime:
        today = datetime.now()
        target_index = list(calendar.day_name).index(day_name)
        days_ahead = (target_index - today.weekday() + 7) % 7
        if days_ahead == 0:
            days_ahead = 7
        return today + timedelta(days=days_ahead)
