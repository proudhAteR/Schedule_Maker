import dateparser

from Core.Interface.Extractor import Extractor
from Infrastructure.Utils.Helpers.patterns import DAY_PATTERNS, DAY_MAPPINGS


class DayExtractor(Extractor):
    async def extract(self, sentence: str) -> tuple[str, bool]:
        lowered = sentence.lower()
        is_recurring = any(kw in lowered for kw in {"every", "each", "weekly"})

        for pattern in DAY_PATTERNS:
            match = pattern.search(lowered)
            if not match:
                continue

            day_str = match.group("day").strip().lower()

            if day_str in DAY_MAPPINGS:
                return DAY_MAPPINGS[day_str], is_recurring

            parsed_day = dateparser.parse(day_str)
            if parsed_day:
                return parsed_day.strftime("%A"), False

        return dateparser.parse("today").strftime("%A"), False
