from dataclasses import dataclass
from typing import ClassVar

from Core.Models.Enum.Priority import Priority
from Core.Models.Events.Event import Event


@dataclass
class Appointment(Event):
    description: str = ''
    color: Priority = Priority.HIGH
    related: ClassVar[list[str]] = ["appointment", "doctor", "dentist", "therapy", "consultation", "info"]

    def to_google_event(self) -> dict:
        event = super().to_google_event()
        if self.description:
            event["description"] = f"Appointment with: {self.description}"
        return event
