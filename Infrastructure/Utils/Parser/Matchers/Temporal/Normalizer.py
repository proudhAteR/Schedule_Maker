import re


class Normalizer:

    def __init__(self, expr: dict):
        self.expressions = expr
        self.patterns = {
            "am": re.compile(r'\b(a\.m\.|a m|am)\b', re.IGNORECASE),
            "pm": re.compile(r'\b(p\.m\.|p m|pm)\b', re.IGNORECASE),
            "dot_time": re.compile(r'(\d{1,2})\.(\d{2})'),
            "colon_spacing": re.compile(r"(\d{1,2})\s*:\s*(\d{2})"),
            "range_sep": re.compile(r'\bto\b|\s*([–—\-])\s*'),
            "trailing_punc": re.compile(r'[.,;:]$'),
            "tight_meridiem": re.compile(r'(\d)(am|pm)\b'),
            "article_the": re.compile(r"\bthe\s+(?=\w+)", re.IGNORECASE),
            "whitespace": re.compile(r"\s+"),
        }
        self.word_to_digit = {
            'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
            'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
        }

        self.word_to_digit_patterns = {
            re.compile(rf'\b{word}\b'): digit
            for word, digit in self.word_to_digit.items()
        }

        self.expr_patterns = {
            re.compile(rf"(?<!\w){re.escape(k)}(?!\w)"): v
            for k, v in expr.items()
        }

    def run(self, sentence: str) -> str:
        normalized = sentence.lower()
        p = self.patterns

        normalized = p["am"].sub('am', normalized)
        normalized = p["pm"].sub('pm', normalized)
        normalized = p["dot_time"].sub(r'\1:\2', normalized)
        normalized = p["colon_spacing"].sub(r"\1:\2", normalized)
        normalized = p["range_sep"].sub(' to ', normalized)

        for pattern, digit in self.word_to_digit_patterns.items():
            normalized = pattern.sub(digit, normalized)

        normalized = p["trailing_punc"].sub('', normalized)
        normalized = p["tight_meridiem"].sub(r'\1 \2', normalized)
        normalized = p["article_the"].sub('', normalized)

        for pattern, repl in self.expr_patterns.items():
            normalized = pattern.sub(repl, normalized)

        normalized = p["whitespace"].sub(" ", normalized).strip()

        return normalized
