from re import *

from Core.Interface.Extractor import Extractor
from Infrastructure.Utils.Helpers.patterns import TIME_EXPRESSIONS, TIME_PATTERNS
from Infrastructure.Utils.Parser.Matchers.Temporal.Extractors.Helpers.MeridiemHelper import MeridiemHelper
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class TimeExtractor(Extractor):
    def __init__(self, time_only_pattern: Pattern):
        self.patterns = TIME_PATTERNS
        self.expressions = TIME_EXPRESSIONS
        self.time_only_pattern = time_only_pattern
        self.number_pattern = compile(r"\b(\d{1,2}(?::\d{2})?)\b")
        self.meridiem_helper = MeridiemHelper()

    async def extract(self, sentence: str) -> tuple[str | None, str | None]:
        sentence = self._sanitize(sentence)

        for idx, pattern in enumerate(self.patterns):
            p_match = pattern.search(sentence)
            if p_match:
                return self._handle_pattern_match(p_match, idx)

        return self._fallback_time_extraction(sentence)

    @staticmethod
    def _sanitize(sentence: str) -> str:
        return sentence.replace(".", "")

    def _handle_pattern_match(self, p_match: Match, idx: int) -> tuple[str, str]:
        raw_start, raw_end = TimeParser.pattern(p_match, idx)
        return self._normalize_time_pair(raw_start, raw_end)

    def _normalize_time_pair(self, start_raw: str, end_raw: str) -> tuple[str, str]:
        start = self.meridiem_helper.normalize(start_raw, end_raw, is_start=True)
        end = self.meridiem_helper.normalize(end_raw, start_raw, is_start=False)
        return start, end

    def _fallback_time_extraction(self, sentence: str) -> tuple[str | None, str | None]:
        p_match = self.time_only_pattern.findall(sentence)
        if len(p_match) >= 2:
            return f"{p_match[0][0]} {p_match[0][1]}", f"{p_match[1][0]} {p_match[1][1]}"

        numbers = self.number_pattern.findall(sentence)
        if len(numbers) >= 2:
            return self.meridiem_helper.infer(numbers[0], numbers[1], sentence)

        return None, None
