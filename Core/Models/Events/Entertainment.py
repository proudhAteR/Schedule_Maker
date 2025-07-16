from Core.Models.Enum.Priority import Priority
from Core.Models.Events.Event import Event


from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Entertainment(Event):
    performer: str = ''
    color: Priority = Priority.CASUAL
    related: ClassVar[list[str]] = [
        "concert", "movie", "theatre", "show", "comedy", "opera", "festival", "screening", "break"
    ]

    def to_google_event(self) -> dict:
        event = super().to_google_event()
        if self.performer:
            event["description"] = f"Featuring: {self.performer}"
        return event
