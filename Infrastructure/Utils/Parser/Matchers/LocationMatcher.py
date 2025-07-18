import re

from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field


class LocationMatcher(Matcher):

    async def match(self, sentence: str) -> dict[Field, str]:
        location_match = re.search(r"(?:in|at) (.*?) from", sentence)
        location = location_match.group(1).strip() if location_match else ""

        return {Field.LOCATION: location}
