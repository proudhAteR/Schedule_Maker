from re import *

from Core.Interface.Extractor import Extractor
from Infrastructure.Utils.Helpers.Patterns.Regex.patterns import TIME_PATTERNS
from Infrastructure.Utils.Helpers.Patterns.patterns import TIME_EXPRESSIONS
from Infrastructure.Utils.Matchers.Time._internal.Extractors.Helpers.MeridiemHelper import MeridiemHelper
from Infrastructure.Utils.Parsers.TimeParser import TimeParser


class TimeExtractor(Extractor):
    def __init__(self, time_only_pattern: Pattern):
        self.patterns = TIME_PATTERNS
        self.expressions = TIME_EXPRESSIONS
        self.time_only_pattern = time_only_pattern
        self.number_pattern = compile(r"\b(\d{1,2}(?::\d{2})?)\b")
        self.meridiem_helper = MeridiemHelper()

    async def extract(self, sentence: str) -> tuple:
        sentence = self._sanitize(sentence)

        for idx, pattern in enumerate(self.patterns):
            p_match = pattern.search(sentence)
            if p_match:
                return self._handle_pattern_match(p_match, idx)

        return self._fallback_time_extraction(sentence)

    @staticmethod
    def _sanitize(sentence: str) -> str:
        return sentence.replace(".", "")

    def _handle_pattern_match(self, p_match: Match, idx: int) -> tuple:
        raw_start, raw_end = TimeParser.pattern(p_match, idx)
        return self._normalize_time_pair(raw_start, raw_end)

    def _normalize_time_pair(self, start_raw: str, end_raw: str) -> tuple:
        start = self.meridiem_helper.normalize(start_raw, end_raw, is_start=True)
        end = self.meridiem_helper.normalize(end_raw, start_raw, is_start=False)
        return start, end

    def _fallback_time_extraction(self, sentence: str) -> tuple:
        p_match = self.time_only_pattern.findall(sentence)
        if len(p_match) >= 2:
            return f"{p_match[0][0]} {p_match[0][1]}", f"{p_match[1][0]} {p_match[1][1]}"

        numbers = self.number_pattern.findall(sentence)
        if len(numbers) >= 2:
            return self.meridiem_helper.infer(numbers[0], numbers[1], sentence)

        return None, None
