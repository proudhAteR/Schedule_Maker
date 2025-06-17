from dataclasses import dataclass

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
                f'RRULE:FREQ=WEEKLY;COUNT={self.period.streak}'
            ]
        }
