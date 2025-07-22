import re

from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field


class TitleMatcher(Matcher):
    async def match(self, tokens: dict) -> dict:
        sentence = tokens.get('title', '')
        title = await self.__process(sentence)

        return {Field.TITLE: title}

    @staticmethod
    async def __process(sentence):
        # Metadata keywords where title usually ends
        split_keywords = r"\b(from|at|in|on|every|by|with|between)\b"
        # Split on first keyword occurrence (start of metadata)
        parts = re.split(split_keywords, sentence, maxsplit=1, flags=re.IGNORECASE)
        raw_title = parts[0].strip()

        # Remove trailing conjunctions/prepositions or punctuation left behind
        raw_title = re.sub(
            r"[\s,:;-]+$",
            "",
            raw_title
        )
        return raw_title.strip().title()
