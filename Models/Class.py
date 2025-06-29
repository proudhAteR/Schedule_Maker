from dataclasses import dataclass
from Models.Event import Event
import re
from Models.Period import Period
from Models.Session import Session
from Models.Enum.Day import Day


@dataclass
class Class(Event):
    teacher: str = ''

    def to_google_event(self) -> dict:
        event = super().to_google_event()
        event["description"] = f"Teacher: {self.teacher}"
        return event

    @classmethod
    def from_sentence(cls, sentence: str, session: Session | None = None) -> "Class":
        pattern = r"(.+?) in (.+?) from (.+?) to (.+?) every (.+?) by (.+)"
        match = re.match(pattern, sentence.strip())
        if not match:
            raise ValueError

        name, location, start, end, day_str, teacher = match.groups()
        day = Day[day_str.strip().upper()]
        period = Period(start.strip(), end.strip(), day, session=session)

        return Class(name.strip(), period, location.strip(), teacher=teacher.strip())
