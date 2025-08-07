from dataclasses import dataclass
from datetime import datetime

from Core.Models.Enum.Field import Field


@dataclass
class Match:
    title: str
    location: str
    start: datetime
    end: datetime
    day_str: str
    extra: str

    @classmethod
    def from_data(cls, data: dict) -> "Match":
        return Match(
            title=data.get(Field.TITLE, ''),
            location=data.get(Field.LOCATION, ''),
            start=data.get(Field.START),
            end=data.get(Field.END),
            day_str=data.get(Field.DAY, ''),
            extra=data.get(Field.EXTRA, '')
        )
