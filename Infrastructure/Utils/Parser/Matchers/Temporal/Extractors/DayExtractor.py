import re
import dateparser
from datetime import datetime

from Core.Interface.Extractor import Extractor

DAY_PATTERNS = [
    re.compile(
        r"\b(?:every|on|this|next)?\s*"
        r"(?P<day>mon(?:day)?|tue(?:s|sday)?|wed(?:nesday)?|thu(?:rs|rsday)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?)s?\b",
        re.IGNORECASE
    ),
    re.compile(
        r"\b(?P<day>today|tomorrow|tonight|yesterday|day after tomorrow|day before yesterday|this weekend|next week|this week|next weekend)\b",
        re.IGNORECASE
    ),
]

DAY_MAPPINGS = {
    # Weekdays (lowercased for matching)
    'mon': 'Monday', 'monday': 'Monday',
    'tue': 'Tuesday', 'tues': 'Tuesday', 'tuesday': 'Tuesday',
    'wed': 'Wednesday', 'weds': 'Wednesday', 'wednesday': 'Wednesday',
    'thu': 'Thursday', 'thurs': 'Thursday', 'thursday': 'Thursday',
    'fri': 'Friday', 'friday': 'Friday',
    'sat': 'Saturday', 'saturday': 'Saturday',
    'sun': 'Sunday', 'sunday': 'Sunday',
}


class DayExtractor(Extractor):
    async def extract(self, sentence: str) -> str | tuple:
        for pattern in DAY_PATTERNS:
            match = pattern.search(sentence)
            if match:
                day_part = match.group("day").lower().strip()
                if day_part in DAY_MAPPINGS:
                    return DAY_MAPPINGS[day_part]

                parsed = dateparser.parse(day_part)
                if parsed:
                    return parsed.strftime("%A")

        return ""