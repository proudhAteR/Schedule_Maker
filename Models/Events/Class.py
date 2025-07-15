from dataclasses import dataclass
from Models.Events.Event import Event
import re
from Models.Recurrence import Recurrence


@dataclass
class Class(Event):
    teacher: str = ''

    def to_google_event(self) -> dict:
        event = super().to_google_event()
        event["description"] = f"Teacher: {self.teacher}"
        return event

    @classmethod
    def from_sentence(cls, sentence: str, recurrence: Recurrence | None = None) -> "Class":
        event = super().from_sentence(sentence, recurrence)
        teacher = cls.__teacher(sentence)

        return cls(
            event.name,
            event.period,
            event.location,
            teacher
        )

    @classmethod
    def __teacher(cls, sentence: str) -> str:
        pattern = r"\bby\s+(.+)"
        match = re.search(pattern, sentence.strip(), re.IGNORECASE)

        if not match:
            return ''

        return match.group(1).strip()
