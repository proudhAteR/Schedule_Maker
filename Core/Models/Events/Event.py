from dataclasses import dataclass
from typing import Type
from Core.Models.Enum.Priority import Priority
from Core.Models.Period import Period


@dataclass
class Event:
    name: str
    period: Period
    location: str
    description: str = ''
    timezone: str = "America/Toronto"
    priority: Priority = Priority.MEDIUM

    # noinspection PyTypeChecker
    def to_google_event(self) -> dict:
        event = {
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
            'colorId': self.priority.value,
        }

        if self.period.streak > 1:
            event['recurrence'] = [
                f'RRULE:FREQ=WEEKLY;COUNT={self.period.streak}'
            ]

        return event

    @classmethod
    def _all_subclasses(cls) -> list[Type['Event']]:
        def recurse(sub):
            return [sub] + [g for sc in sub.__subclasses__() for g in recurse(sc)]

        subclasses = recurse(cls)
        return subclasses

    @classmethod
    def detect_type(cls, sentence: str) -> type['Event']:
        lowered = sentence.lower()

        for subclass in cls._all_subclasses():
            related = getattr(subclass, 'related', [])
            if any(word in lowered for word in related):
                return subclass

        return cls
