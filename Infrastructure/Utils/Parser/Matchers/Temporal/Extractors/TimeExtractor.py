import re

from Core.Interface.Extractor import Extractor
from Infrastructure.Utils.Parser.Matchers.Temporal.Extractors.Helpers.MeridiemHelper import MeridiemHelper
from Infrastructure.Utils.Parser.TimeParser import TimeParser

TIME_PATTERNS = [
    # Natural language patterns first (higher priority)
    re.compile(
        r"\b(?:from|starting(?:\s+at)?|begins?(?:\s+at)?)\s+(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\s+(?:to|until|through|ending(?:\s+at)?|till)\s+(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\b",
        re.IGNORECASE),

    # Time ranges with meridiem
    re.compile(r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\s*(?:to|until|through|-|–|—)\s*(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
               re.IGNORECASE),

    # Single meridiem shared between times
    re.compile(r"\b(\d{1,2}(?::\d{2})?)\s*(?:to|until|through|-|–|—)\s*(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
               re.IGNORECASE),

    # 24-hour formats
    re.compile(r"\b([01]?\d|2[0-3]):([0-5]\d)\s*(?:to|until|through|-|–|—)\s*([01]?\d|2[0-3]):([0-5]\d)\b",
               re.IGNORECASE),
    re.compile(r"\b([01]?\d|2[0-3])\s*(?:to|until|through|-|–|—)\s*([01]?\d|2[0-3])\b", re.IGNORECASE),

    # Contextual patterns
    re.compile(
        r"\b(?:between|from)\s+(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\s+(?:and|to|until)\s+(\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)\b",
        re.IGNORECASE),
    # Matches "at 2:00 pm", "in 2:00 pm", "on 2:00 pm"
    re.compile(
        r"\b(?:at|in|on|around|about)?\s*(\d{1,2}(?::\d{2})?)\s*(am|pm)\b",
        re.IGNORECASE
    ),

]


class TimeExtractor(Extractor):
    def __init__(self, expressions: dict, time_only_pattern: re.Pattern):
        self.patterns = TIME_PATTERNS
        self.expressions = expressions
        self.time_only_pattern = time_only_pattern
        self.number_pattern = re.compile(r"\b(\d{1,2}(?::\d{2})?)\b")
        self.meridiem_helper = MeridiemHelper()

    async def extract(self, sentence: str) -> tuple[str | None, str | None]:
        sentence = self._sanitize(sentence)

        for idx, pattern in enumerate(self.patterns):
            if match := pattern.search(sentence):
                return self._handle_pattern_match(match, idx)

        return self._fallback_time_extraction(sentence)

    @staticmethod
    def _sanitize(sentence: str) -> str:
        return sentence.replace(".", "")

    def _handle_pattern_match(self, match: re.Match, idx: int) -> tuple[str, str]:
        raw_start, raw_end = TimeParser.pattern(match, idx)
        return self._normalize_time_pair(raw_start, raw_end)

    def _normalize_time_pair(self, start_raw: str, end_raw: str) -> tuple[str, str]:
        start = self.meridiem_helper.normalize(start_raw, end_raw, is_start=True)
        end = self.meridiem_helper.normalize(end_raw, start_raw, is_start=False)
        return start, end

    def _fallback_time_extraction(self, sentence: str) -> tuple[str | None, str | None]:
        if (matches := self.time_only_pattern.findall(sentence)) and len(matches) >= 2:
            return f"{matches[0][0]} {matches[0][1]}", f"{matches[1][0]} {matches[1][1]}"

        if (numbers := self.number_pattern.findall(sentence)) and len(numbers) >= 2:
            return self.meridiem_helper.infer(numbers[0], numbers[1], sentence)

        return None, None
