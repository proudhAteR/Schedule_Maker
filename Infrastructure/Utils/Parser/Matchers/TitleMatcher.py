import re

from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field


class TitleMatcher(Matcher):
    async def match(self, sentence: str) -> dict[Field, str]:
        split_keywords = r"\b(?:in|at|from|on|every|by|with)\b"
        parts = re.split(split_keywords, sentence, maxsplit=1, flags=re.IGNORECASE)
        event_name = parts[0].strip()
        event_name = re.sub(r"\b\d{1,2}(:\d{2})?(\s*[-toand]+\s*\d{1,2}(:\d{2})?)?\s*(am|pm)?\b$", "", event_name,
                            flags=re.IGNORECASE).strip()

        return {Field.NAME: event_name}
