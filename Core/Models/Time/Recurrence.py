from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Recurrence:
    first_occurrence: datetime = field(default_factory=datetime.now)
    streak: int = 15

    @classmethod
    def update_from(cls, prev: Recurrence | None, day_str: str | None) -> Recurrence:
        if not day_str:
            return cls(streak=1)
        return prev or cls()
