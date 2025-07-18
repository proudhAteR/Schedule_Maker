import re


class Normalizer:

    def __init__(self, expr: dict):
        self.expressions = expr

    def run(self, sentence: str) -> str:
        normalized = sentence.lower()

        # Standardize meridiem (am/pm) with dots and spaces
        normalized = re.sub(r'\b(a\.m\.|a m|am)\b', 'am', normalized)
        normalized = re.sub(r'\b(p\.m\.|p m|pm)\b', 'pm', normalized)

        # Replace dotted times like 3.30 with 3:30
        normalized = re.sub(r'(\d{1,2})\.(\d{2})', r'\1:\2', normalized)
        normalized = re.sub(r"(\d{1,2})\s*:\s*(\d{2})", r"\1:\2", normalized)

        # Normalize spacing around time range separators
        normalized = re.sub(r'\s*(to|–|—|-)\s*', ' to ', normalized)

        # Replace spelled-out numbers (optional)
        word_to_digit = {
            'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
            'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
        }
        for word, digit in word_to_digit.items():
            normalized = re.sub(rf'\b{word}\b', digit, normalized)

        # Remove trailing punctuation that can interfere
        normalized = re.sub(r'[.,;:]$', '', normalized)

        # Normalize AM/PM spacing, e.g. "3pm" -> "3 pm"
        normalized = re.sub(r'(\d)(am|pm)\b', r'\1 \2', normalized)

        # Normalize common time expressions
        for expr, replacement in self.expressions.items():
            normalized = re.sub(rf"\b{expr}\b", replacement, normalized)

        # Clean up extra whitespace
        normalized = re.sub(r"\s+", " ", normalized).strip()

        return normalized
