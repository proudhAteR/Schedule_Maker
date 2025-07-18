import re

from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field


class TitleMatcher(Matcher):
    async def match(self, sentence: str) -> dict[Field, str]:
        # Metadata keywords where title usually ends
        split_keywords = r"\b(from|at|in|on|every|by|with|between)\b"

        # Split on first keyword occurrence (start of metadata)
        parts = re.split(split_keywords, sentence, maxsplit=1, flags=re.IGNORECASE)
        raw_title = parts[0].strip()

        # Remove trailing times or time ranges inside the title
        raw_title = re.sub(
            r"\b\d{1,2}(:\d{2})?\s*(?:[-–—toand]{1,4})?\s*\d{1,2}(:\d{2})?\s*(am|pm)?\b",
            "",
            raw_title,
            flags=re.IGNORECASE
        )

        # Remove single trailing times like "9am" or "17:00"
        raw_title = re.sub(
            r"\b\d{1,2}(:\d{2})?\s*(am|pm)?\b$",
            "",
            raw_title,
            flags=re.IGNORECASE
        )

        # Remove trailing dangling metadata keywords that may remain
        raw_title = re.sub(
            r"\b(from|at|in|on|every|by|with)$",
            "",
            raw_title,
            flags=re.IGNORECASE
        )

        # Remove trailing conjunctions/prepositions or punctuation left behind
        raw_title = re.sub(
            r"[\s,:;-]+$",
            "",
            raw_title
        )

        return {Field.NAME: raw_title.strip()}
