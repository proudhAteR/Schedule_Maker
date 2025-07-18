import re

from Core.Interface.Extractor import Extractor

# Enhanced day patterns with better context awareness
DAY_PATTERNS = [
    # Explicit day mentions with context
    re.compile(r"\b(?:every|on|this|next)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
               re.IGNORECASE),
    re.compile(r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)s?\b", re.IGNORECASE),
    # Shortened versions
    re.compile(r"\b(?:every|on|this|next)?\s*(mon|tue|tues|wed|weds|thu|thurs|fri|sat|sun)(?:day)?s?\b",
               re.IGNORECASE),
]

# Day name mappings
DAY_MAPPINGS = {
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
        """Extract day with improved pattern matching."""

        for pattern in DAY_PATTERNS:
            match = pattern.search(sentence)
            if match:
                day_part = match.group(1).lower()
                return DAY_MAPPINGS.get(day_part, "")
        return ""
