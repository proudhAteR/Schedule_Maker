from dataclasses import dataclass
from typing import ClassVar

from Core.Models.Events.Event import Event


@dataclass
class Class(Event):
    teacher: str = ''
    related: ClassVar[list[str]] = ["class", "lecture", "lab", "exam", "lesson"]

    def to_google_event(self) -> dict:
        event = super().to_google_event()
        event["description"] = f"Teacher: {self.teacher}"
        return event
