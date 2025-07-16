from dataclasses import dataclass
from typing import ClassVar

from Core.Models.Enum.Priority import Priority
from Core.Models.Events.Event import Event


@dataclass
class Meeting(Event):
    priority: Priority = Priority.HIGH
    description: str = ''
    related: ClassVar[list[str]] = ["meeting", "sync", "standup", "presentation"]

    def to_google_event(self) -> dict:
        event = super().to_google_event()
        if self.description:
            event["description"] = f"Organizer: {self.description}"
        return event
