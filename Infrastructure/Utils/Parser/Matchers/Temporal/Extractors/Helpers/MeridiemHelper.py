import re


class MeridiemHelper:
    meridiem_pattern = re.compile(r"\b(am|pm)\b", re.IGNORECASE)

    def normalize(self, time: str, other_time: str, is_start: bool) -> str:
        if self._has_meridiem(time) or self._is_24_hour_format(time):
            return time

        hour = self._extract_hour(time)
        other_hour = self._extract_hour(other_time)
        other_mer = self._get_meridiem(other_time)

        if other_mer:
            return self._infer_from_other_meridiem(hour, other_hour, other_mer, time, is_start)

        return self._infer_from_context(hour, time, is_start)

    def infer(self, start: str, end: str, context: str) -> tuple[str, str]:
        start_hour = int(start.split(':')[0])
        end_hour = int(end.split(':')[0])

        if start_hour > 12 or end_hour > 12 or '24' in context or 'military' in context:
            return self._format_24_hour(start), self._format_24_hour(end)

        start_meridiem = self._infer_contextual_meridiem(start_hour, context)
        end_meridiem = self._infer_contextual_meridiem(end_hour, context)

        return f"{start} {start_meridiem}", f"{end} {end_meridiem}"

    # Helper Methods Below

    # noinspection t
    @staticmethod
    def _infer_from_other_meridiem(hour, other_hour, other_mer, time, is_start):
        other_mer = other_mer.lower()
        if is_start:
            if hour < other_hour and other_mer == "pm":
                return f"{time} pm"
            if hour > other_hour and other_mer == "am":
                return f"{time} am"
        else:
            if hour > other_hour and other_mer == "am":
                return f"{time} am"
            if hour < other_hour and other_mer == "pm":
                return f"{time} pm"

        return f"{time} {'am' if hour <= 11 else 'pm'}"

    @staticmethod
    def _infer_from_context(hour, time, is_start):
        if hour <= 7:
            return f"{time} {'am' if is_start else 'pm'}"
        if hour <= 11:
            return f"{time} am"
        return f"{time} pm"

    @staticmethod
    def _infer_contextual_meridiem(hour, context):
        if any(word in context.lower() for word in ['morning', 'am', 'early']):
            return 'am'
        if any(word in context.lower() for word in ['afternoon', 'evening', 'pm', 'late']):
            return 'pm'
        return 'am' if hour <= 11 else 'pm'

    @staticmethod
    def _format_24_hour(time_str):
        return f"{time_str}:00" if ':' not in time_str else time_str

    @staticmethod
    def _extract_hour(time_str: str) -> int:
        match = re.match(r"(\d{1,2})", time_str)
        return int(match.group(1)) if match else 0

    def _get_meridiem(self, time_str: str) -> str | None:
        match = self.meridiem_pattern.search(time_str)
        return match.group(1) if match else None

    def _has_meridiem(self, time_str: str) -> bool:
        return bool(self.meridiem_pattern.search(time_str))

    @staticmethod
    def _is_24_hour_format(time_str: str) -> bool:
        return bool(re.match(r"^([01]?\d|2[0-3])(:[0-5]\d)?$", time_str))
