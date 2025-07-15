from enum import Enum


class Priority(str, Enum):
    URGENT = "11"
    HIGH = "4"
    MEDIUM = "9"
    MINOR = "8"
    SOFT = "10"
    CASUAL = "1"
    OPTIONAL = "5"

    @classmethod
    def from_str(cls, string: str) -> "Priority":
        s = string.upper()
        for priority in cls:
            if priority.name == s :
                return priority

        return Priority.CASUAL
