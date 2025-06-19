from datetime import datetime, timedelta

from Models.Session import Session
from Models.enum.Day import Day


def _str_to_datetime(t: str, day: Day, session_start: datetime | None = None) -> datetime:
    if session_start is None:
        session_start = datetime.now()
    weekday_diff = (day.value - session_start.weekday() + 7) % 7
    target_date = session_start + timedelta(days=weekday_diff)
    return datetime.combine(target_date.date(), datetime.strptime(t, "%H:%M").time())


class Period:
    def __init__(self, start: str, end: str, day: Day, session: Session | None = None, streak: int = 15):
        self.day = day
        self.streak = session.streak if session else streak
        start_date = session.first_occurrence if session else None
        end_date = session.first_occurrence if session else None

        self.start = _str_to_datetime(start, day, session_start=start_date)
        self.end = _str_to_datetime(end, day, session_start=end_date)
