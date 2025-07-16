from dataclasses import dataclass
from Core.Models.Enum.Priority import Priority
from Core.Models.Period import Period


@dataclass
class Event:
    name: str
    period: Period
    location: str
    description: str = ''
    timezone: str = "America/Toronto"
    color: Priority = Priority.CASUAL

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
            'colorId': self.color.value,
        }

        if self.period.streak > 1:
            event['recurrence'] = [
                f'RRULE:FREQ=WEEKLY;COUNT={self.period.streak}'
            ]

        return event
