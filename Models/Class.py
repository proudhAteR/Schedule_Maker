from dataclasses import dataclass
from Models.Event import Event
import re
from Models.Period import Period
from Models.enum.Day import Day


@dataclass
class Class(Event):
    teacher: str = ''

    def to_google_event(self) -> dict:
        event = super().to_google_event()
        event["description"] = f"Teacher: {self.teacher}"
        return event

    @classmethod
    def from_sentence(cls, sentence: str) -> "Class":
        pattern = r"(.+?) IN (.+?) FROM (.+?) TO (.+?) EVERY (.+?) BY (.+)"
        match = re.match(pattern, sentence.strip())
        if not match:
            raise ValueError("Sentence format is invalid")

        name, location, start, end, day_str, teacher = match.groups()
        day_enum = Day[day_str.strip().upper()]
        period = Period(start=start.strip(), end=end.strip(), day=day_enum)
        return cls(name=name.strip(), location=location.strip(), period=period, teacher=teacher.strip())
