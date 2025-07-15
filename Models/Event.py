from dataclasses import dataclass
import re
from datetime import datetime

from Models.Recurrence import Recurrence
from Models.Enum.Day import Day
from Models.Period import Period


@dataclass
class Event:
    name: str
    period: Period
    location: str
    description: str = ''
    timezone: str = "America/Toronto"

    def to_google_event(self) -> dict:
        return {
            'summary': self.name,
            'location': self.location,
            'description': self.description,
            'start': {
                'dateTime': self.period.start.isoformat(),
                'timeZone': self.timezone,
            },
            'end': {
                'dateTime': self.period.end.isoformat(),
                'timeZone': self.timezone,
            },
            'recurrence': [
                f'RRULE:FREQ=WEEKLY;'
                f'COUNT={self.period.streak}'
            ]
        }

    @classmethod
    def from_sentence(cls, sentence: str, recurrence: Recurrence | None = None) -> "Event":
        name, location, start, end, day_str, _ = cls._pattern_match(sentence)
        day, recurrence = cls.__recurrence_gestion(day_str, recurrence)
        period = Period(
            start.strip(),
            end.strip(),
            day,
            recurrence
        )

        return cls(name.strip(), period, location.strip())

    @classmethod
    def _pattern_match(cls, sentence: str) -> tuple:
        pattern = r"^(.*?) in (.*?) from (.*?) to (.*?)(?: every (.*?))?(?: by (.*))?$"
        match = re.match(pattern, sentence.strip())

        if not match:
            raise ValueError("Sentence format invalid.")

        return tuple(part or "" for part in match.groups())

    @classmethod
    def __recurrence_gestion(cls, day_str: str | None, recurrence: Recurrence | None) -> tuple:
        recurrence = recurrence or Recurrence(datetime.now(), streak=15)
        day = Period.today()

        if not day_str:
            return day, Recurrence(datetime.now(), 1)

        try:
            day_str = day_str.strip().upper()
            day = Day[day_str]
        except KeyError:
            raise ValueError(f"Unknown day: {day_str}")

        return day, recurrence
