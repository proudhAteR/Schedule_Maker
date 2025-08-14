import dateparser

from Core.Interface.Extractor import Extractor
from Infrastructure.Utils.Helpers.Patterns.Regex.patterns import DAY_PATTERNS, DAY_MAPPINGS


class DayExtractor(Extractor):
    async def extract(self, sentence: str) -> tuple:
        lowered = sentence.lower()
        is_recurring = any(kw in lowered for kw in {"every", "each", "weekly"})

        for pattern in DAY_PATTERNS:
            match = pattern.search(lowered)
            if not match:
                continue

            day_str = match.group("day").strip().lower()
            parsed_day = dateparser.parse(
                DAY_MAPPINGS.get(day_str, day_str)
            )

            if parsed_day:
                return parsed_day, is_recurring if day_str in DAY_MAPPINGS else False

        return dateparser.parse("today"), False
