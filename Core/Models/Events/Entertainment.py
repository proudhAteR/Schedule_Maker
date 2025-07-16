from dataclasses import dataclass
from typing import ClassVar

from Core.Models.Enum.Priority import Priority
from Core.Models.Events.Event import Event


@dataclass
class Entertainment(Event):
    description: str = ''
    color: Priority = Priority.OPTIONAL
    related: ClassVar[list[str]] = [
        "concert", "movie", "theatre", "show", "comedy", "opera", "festival", "screening", "break"
    ]

    def to_google_event(self) -> dict:
        event = super().to_google_event()
        if self.description:
            event["description"] = f"Featuring: {self.description}"
        return event
