from enum import Enum


class Priority(str, Enum):
    URGENT = "11"  # Red — Critical or emergency-level tasks
    HIGH = "4"  # Pink — Important or time-sensitive
    NORMAL = "9"  # Blue — Normal or default importance
    CASUAL = "1"  # Lavender — Non-work or casual meetings
    OPTIONAL = "5"  # Yellow — Optional activities

    @classmethod
    def from_str(cls, string: str) -> "Priority":
        s = string.upper()
        for priority in cls:
            if priority.name == s:
                return priority

        return Priority.NORMAL
