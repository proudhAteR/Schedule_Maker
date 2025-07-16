import re

from Core.Interface.Matcher import Matcher


class ExtraMatcher(Matcher):

    def match(self,sentence: str) -> str:
        by_match = re.search(r"(?:\bby|\bwith)\s+(.+)", sentence, re.IGNORECASE)
        more = by_match.group(1).strip() if by_match else ""
        return more
