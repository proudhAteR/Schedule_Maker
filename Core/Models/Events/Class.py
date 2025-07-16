from dataclasses import dataclass
from Core.Models.Events.Event import Event


@dataclass
class Class(Event):
    teacher: str = ''

    def to_google_event(self) -> dict:
        event = super().to_google_event()
        event["description"] = f"Teacher: {self.teacher}"
        return event
