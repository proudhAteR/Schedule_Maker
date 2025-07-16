import re

from Core.Interface.Matcher import Matcher


class LocationMatcher(Matcher):

    def match(self, sentence: str) -> str | tuple:
        location_match = re.search(r"(?:in|at) (.*?) from", sentence)
        location = location_match.group(1).strip() if location_match else ""
        return location
