import re

import dateparser

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
    async def extract(self, sentence: str) -> tuple[str, bool]:
        lowered = sentence.lower()
        recurring_keywords = {"every", "each", "weekly"}
        is_recurring = any(word in lowered for word in recurring_keywords)

        for pattern in DAY_PATTERNS:
            match = pattern.search(lowered)
            if not match:
                continue

            day_part = match.group("day").lower().strip()

            # Direct mapping
            if day_part in DAY_MAPPINGS:
                return DAY_MAPPINGS[day_part], is_recurring

            # Parsed with dateparser (e.g., "tomorrow", "next weekend")
            parsed = dateparser.parse(day_part)
            if parsed:
                return parsed.strftime("%A"), False  # parsed values are assumed one-time

        return "", False
