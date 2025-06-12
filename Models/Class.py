from dataclasses import dataclass
import Period

@dataclass
class Class:
    name: str
    teacher: str
    location: str
    period: Period
