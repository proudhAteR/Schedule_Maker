from datetime import datetime

from Core.Models.Enum.Field import Field
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class FallbackHandler:
    def __init__(self, expressions: dict):
        self.time_only_pattern = None
        self.parser = TimeParser()
        self.expressions = expressions

    def handle(self, sentence: str, day_str: str) -> dict:
        """Handle fallback cases when time extraction fails."""
        # Try to extract any time information for fallback
        fallback_time = self._extract_any_time(sentence)
        if not fallback_time:
            fallback_time = datetime.now()

        return {
            Field.DAY: day_str,
            Field.START: fallback_time,
            Field.END: fallback_time,
        }

    def _extract_any_time(self, sentence: str) -> datetime | None:
        """Extract any time information as fallback."""
        # Look for any time patterns
        times = self.time_only_pattern.findall(sentence)
        if times:
            time_str = f"{times[0][0]} {times[0][1]}"
            return self.parser.parse(time_str)

        # Look for time expressions
        for expr, replacement in self.expressions.items():
            if expr in sentence.lower():
                return self.parser.parse(replacement)

        return None
