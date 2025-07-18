import re

from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field


class ExtraMatcher(Matcher):

    async def match(self, sentence: str) -> dict[Field, str]:
        by_match = re.search(r"(?:\bby|\bwith)\s+(.+)", sentence, re.IGNORECASE)
        more = by_match.group(1).strip().title() if by_match else ""

        return {Field.EXTRA: more}
