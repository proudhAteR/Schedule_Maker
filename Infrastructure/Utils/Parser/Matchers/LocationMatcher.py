import re

from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field


class LocationMatcher(Matcher):

    async def match(self, tokens: dict) -> dict:
        sentence = tokens.get('location', '')
        location_match = re.search(
            r"(?:in|at|inside) (.+)$",
            sentence, re.IGNORECASE
        )
        location = location_match.group(1).strip().title() if location_match else ""

        return {Field.LOCATION: location}
