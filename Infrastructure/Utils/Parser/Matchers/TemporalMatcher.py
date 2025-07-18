import calendar
import re
from datetime import datetime, timedelta, time
import dateparser
from Core.Interface.Matcher import Matcher
from Core.Models.Enum.Field import Field


# Used claude and Chatgpt for the logic :3
# noinspection t
class TemporalMatcher(Matcher):
    """Enhanced temporal matcher with improved natural language parsing."""

    # Enhanced day patterns with better context awareness
    DAY_PATTERNS = [
        # Explicit day mentions with context
        re.compile(r"\b(?:every|on|this|next)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
                   re.IGNORECASE),
        re.compile(r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)s?\b", re.IGNORECASE),
        # Shortened versions
        re.compile(r"\b(?:every|on|this|next)?\s*(mon|tue|tues|wed|weds|thu|thurs|fri|sat|sun)(?:day)?s?\b",
                   re.IGNORECASE),
    ]

    # More comprehensive time patterns with better natural language support
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
    ]

    # Common time expressions
    TIME_EXPRESSIONS = {
        'noon': '12:00 pm',
        'midnight': '12:00 am',
        'morning': '9:00 am',
        'afternoon': '2:00 pm',
        'evening': '6:00 pm',
        'night': '9:00 pm',
    }

    # Day name mappings
    DAY_MAPPINGS = {
        'mon': 'Monday', 'monday': 'Monday',
        'tue': 'Tuesday', 'tues': 'Tuesday', 'tuesday': 'Tuesday',
        'wed': 'Wednesday', 'weds': 'Wednesday', 'wednesday': 'Wednesday',
        'thu': 'Thursday', 'thurs': 'Thursday', 'thursday': 'Thursday',
        'fri': 'Friday', 'friday': 'Friday',
        'sat': 'Saturday', 'saturday': 'Saturday',
        'sun': 'Sunday', 'sunday': 'Sunday',
    }

    def __init__(self):
        super().__init__()
        self.meridiem_pattern = re.compile(r"\b(am|pm)\b", re.IGNORECASE)
        self.time_only_pattern = re.compile(r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\b", re.IGNORECASE)
        self.number_pattern = re.compile(r"\b(\d{1,2}(?::\d{2})?)\b")

    async def match(self, sentence: str) -> dict:
        """Parse sentence with enhanced natural language understanding."""
        if not sentence or not sentence.strip():
            now = datetime.now()
            return {Field.DAY: "", Field.START: now, Field.END: now}

        # Normalize the sentence
        normalized = self._normalize_sentence(sentence)

        # Extract components
        day_str = self._extract_day(normalized)
        start_raw, end_raw = self._extract_time_range(normalized)

        # Handle special cases and validation
        if not start_raw or not end_raw:
            return self._handle_fallback(sentence, day_str)

        # Resolve the time range
        start, end = self.resolve_time_range(day_str, start_raw, end_raw)

        return {
            Field.DAY: day_str,
            Field.START: start,
            Field.END: end
        }

    def _normalize_sentence(self, sentence: str) -> str:
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
        for expr, replacement in self.TIME_EXPRESSIONS.items():
            normalized = re.sub(rf"\b{expr}\b", replacement, normalized)

        # Clean up extra whitespace
        normalized = re.sub(r"\s+", " ", normalized).strip()

        return normalized

    def _extract_day(self, sentence: str) -> str:
        """Extract day with improved pattern matching."""
        for pattern in self.DAY_PATTERNS:
            match = pattern.search(sentence)
            if match:
                day_part = match.group(1).lower()
                return self.DAY_MAPPINGS.get(day_part, "")
        return ""

    def _extract_time_range(self, sentence: str) -> tuple:
        """Extract time range with enhanced pattern matching."""
        # Remove periods that might interfere
        clean_sentence = re.sub(r"\.", "", sentence)

        # Try each pattern
        for i, pattern in enumerate(self.TIME_PATTERNS):
            match = pattern.search(clean_sentence)
            if match:
                result = self._process_time_match(match, i)
                if result[0] and result[1]:
                    return self._normalize_time_pair(result[0], result[1])

        # Fallback strategies
        return self._fallback_time_extraction(clean_sentence)

    @staticmethod
    def _process_time_match(match: re.Match, pattern_index: int) -> tuple:
        """Process regex match with better context awareness."""
        groups = match.groups()

        if pattern_index == 0:  # Natural language patterns
            return groups[0].strip(), groups[1].strip()

        elif pattern_index == 1:  # X am to Y pm
            return f"{groups[0]} {groups[1]}", f"{groups[2]} {groups[3]}"

        elif pattern_index == 2:  # X to Y am/pm (shared meridiem)
            return f"{groups[0]} {groups[2]}", f"{groups[1]} {groups[2]}"

        elif pattern_index == 3:  # 24-hour with minutes
            return f"{groups[0]}:{groups[1]}", f"{groups[2]}:{groups[3]}"

        elif pattern_index == 4:  # 24-hour without minutes
            return f"{groups[0]}:00", f"{groups[1]}:00"

        elif pattern_index == 5:  # Between/from patterns
            return groups[0].strip(), groups[1].strip()

        return None, None

    def _fallback_time_extraction(self, sentence: str) -> tuple:
        """Fallback time extraction strategies."""
        # Try to find am/pm times
        times = self.time_only_pattern.findall(sentence)
        if len(times) >= 2:
            return f"{times[0][0]} {times[0][1]}", f"{times[1][0]} {times[1][1]}"

        # Try to find any numeric times
        numbers = self.number_pattern.findall(sentence)
        if len(numbers) >= 2:
            return self._smart_time_inference(numbers[0], numbers[1], sentence)

        return None, None

    @staticmethod
    def _smart_time_inference(start_num: str, end_num: str, context: str) -> tuple:
        """Infer time format based on context and number values."""
        start_hour = int(start_num.split(':')[0])
        end_hour = int(end_num.split(':')[0])

        # Check for 24-hour format indicators
        if start_hour > 12 or end_hour > 12 or '24' in context or 'military' in context:
            return f"{start_num}:00" if ':' not in start_num else start_num, \
                f"{end_num}:00" if ':' not in end_num else end_num

        # Infer am/pm based on context and typical work hours
        def infer_meridiem(hour: int, is_start: bool) -> str:
            if hour <= 7:
                return "am" if is_start else "pm"
            elif hour <= 11:
                return "am"
            elif hour == 12:
                return "pm"
            else:
                return "pm"

        start_meridiem = infer_meridiem(start_hour, True)
        end_meridiem = infer_meridiem(end_hour, False)

        # Check for contextual clues
        if any(word in context for word in ['morning', 'am', 'early']):
            start_meridiem = "am"
        if any(word in context for word in ['afternoon', 'evening', 'pm', 'late']):
            end_meridiem = "pm"

        return f"{start_num} {start_meridiem}", f"{end_num} {end_meridiem}"

    def _normalize_time_pair(self, start_raw: str, end_raw: str) -> tuple:
        """Enhanced time pair normalization."""
        start_raw = start_raw.strip()
        end_raw = end_raw.strip()

        # Apply smart meridiem assignment
        start_normalized = self.smart_meridiem_assignment(start_raw, end_raw, True)
        end_normalized = self.smart_meridiem_assignment(end_raw, start_raw, False)

        return start_normalized, end_normalized

    def resolve_time_range(self, day_str: str, start_raw: str, end_raw: str) -> tuple:
        """Resolve time range with better error handling."""
        base_date = self._get_next_weekday(day_str)

        # Parse times with multiple strategies
        start_time = self._robust_time_parse(start_raw)
        end_time = self._robust_time_parse(end_raw)

        if not start_time or not end_time:
            return base_date, base_date

        start = datetime.combine(base_date.date(), start_time)
        end = datetime.combine(base_date.date(), end_time)

        # Handle overnight periods
        if end <= start:
            end += timedelta(days=1)

        return start, end

    @staticmethod
    def _robust_time_parse(time_str: str) -> time | None:
        if not time_str or not time_str.strip():
            return None

        time_str = time_str.strip()

        # Try parsing with dateparser first
        parsed = dateparser.parse(time_str)
        if parsed:
            # Check if parsed time is midnight AND input looks like an integer hour
            if parsed.time() == time(0, 0) and re.fullmatch(r"\d{1,2}", time_str):
                hour = int(time_str)
                if 0 <= hour <= 23:
                    return time(hour, 0)
                else:
                    return None
            else:
                return parsed.time()

        # Try 24-hour format (e.g. "14:30")
        if re.fullmatch(r"\d{1,2}:\d{2}", time_str):
            try:
                dt = datetime.strptime(time_str, "%H:%M")
                return dt.time()
            except ValueError:
                return None

        # Try 12-hour format with am/pm (e.g. "4:15 pm", "12 am", "5pm")
        match = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)", time_str, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            meridiem = match.group(3).lower()

            if meridiem == "pm" and hour != 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0

            return time(hour, minute)

        # If none of the above matched, return None
        return None

    def _handle_fallback(self, sentence: str, day_str: str) -> dict:
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
            return self._robust_time_parse(time_str)

        # Look for time expressions
        for expr, replacement in self.TIME_EXPRESSIONS.items():
            if expr in sentence.lower():
                return self._robust_time_parse(replacement)

        return None

    @staticmethod
    def _get_next_weekday(day_name: str | None) -> datetime:
        """Get next weekday with better handling."""
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if not day_name or not day_name.strip():
            return base_time

        day_name = day_name.strip().capitalize()

        try:
            target_index = list(calendar.day_name).index(day_name)
            today = datetime.now()
            days_ahead = (target_index - today.weekday() + 7) % 7

            if days_ahead == 0:
                days_ahead = 7  # Get next occurrence

            return base_time + timedelta(days=days_ahead)
        except ValueError:
            return base_time

    def smart_meridiem_assignment(self, time_str: str, other_time: str, is_start: bool) -> str:
        if self.is_24_hour_format(time_str) or self.has_meridiem(time_str):
            return time_str  # DO NOT add am/pm if already 24-hour or has meridiem

        hour = self.get_hour_from_time(time_str)
        other_hour = self.get_hour_from_time(other_time)
        other_mer_match = self.meridiem_pattern.search(other_time)

        def infer_from_other_meridiem():
            other_mer = other_mer_match.group(1).lower()

            if is_start:
                if hour < other_hour and other_mer == "pm":
                    return f"{time_str} pm"
                if hour > other_hour and other_mer == "am":
                    return f"{time_str} am"
                return f"{time_str} {'am' if hour <= 11 else 'pm'}"
            else:
                if hour > other_hour and other_mer == "am":
                    return f"{time_str} am"
                if hour < other_hour and other_mer == "pm":
                    return f"{time_str} pm"
                return f"{time_str} pm"

        if other_mer_match and not self.is_24_hour_format(other_time):
            return infer_from_other_meridiem()

        # Fallback inference
        if hour <= 7:
            return f"{time_str} {'am' if is_start else 'pm'}"
        if hour <= 11:
            return f"{time_str} am"
        return f"{time_str} pm"

    # Helper functions
    @staticmethod
    def is_24_hour_format(time_str: str) -> bool:
        return bool(
            re.match(r"^([01]?\d|2[0-3])(:[0-5]\d)?$", time_str)
        )

    def has_meridiem(self, time_str: str) -> bool:
        return bool(self.meridiem_pattern.search(time_str))

    @staticmethod
    def get_hour_from_time(time_str: str) -> int:
        hour_match = re.match(r"(\d{1,2})", time_str)
        return int(hour_match.group(1)) if hour_match else 0
