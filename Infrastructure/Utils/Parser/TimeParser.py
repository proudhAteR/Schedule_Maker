import re
from datetime import time, datetime

import dateparser

from Core.Interface.Parser import Parser


# noinspection t
class TimeParser(Parser):
    def parse(self, time_str: str):
        if not time_str or not time_str.strip():
            return None

        time_str = time_str.strip()

        # Try parsing with dateparser first
        parsed = dateparser.parse(time_str)
        if parsed:
            # Check if parsed time is midnight AND input looks like an integer hour
            if parsed.time() == time(0, 0) and re.fullmatch(r"\d{1,2}", time_str):
                hour = int(time_str)
                if 0 <= hour <= 23:
                    return time(hour, 0)
                else:
                    return None
            else:
                return parsed.time()

        # Try 24-hour format (e.g. "14:30")
        if re.fullmatch(r"\d{1,2}:\d{2}", time_str):
            try:
                dt = datetime.strptime(time_str, "%H:%M")
                return dt.time()
            except ValueError:
                return None

        # Try 12-hour format with am/pm (e.g. "4:15 pm", "12 am", "5pm")
        match = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)", time_str, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            meridiem = match.group(3).lower()

            if meridiem == "pm" and hour != 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0

            return time(hour, minute)

        # If none of the above matched, return None
        return None

    @staticmethod
    def pattern(match: re.Match, pattern_index: int) -> tuple:
        groups = match.groups()

        match pattern_index:
            case 0 | 5:
                return groups[0].strip(), groups[1].strip()
            case 1:
                return f"{groups[0]} {groups[1]}", f"{groups[2]} {groups[3]}"
            case 2:
                return f"{groups[0]} {groups[2]}", f"{groups[1]} {groups[2]}"
            case 3:
                return f"{groups[0]}:{groups[1]}", f"{groups[2]}:{groups[3]}"
            case 4:
                return f"{groups[0]}:00", f"{groups[1]}:00"
            case 6:
                return f"{groups[0]} {groups[1]}", f"{groups[0]} {groups[1]}"

        return "", ""
