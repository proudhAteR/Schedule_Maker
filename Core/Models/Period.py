from datetime import datetime, timedelta

from Core.Models.Recurrence import Recurrence
from Core.Models.Enum.Day import Day


class Period:
    def __init__(self, start: str, end: str, day: Day, session: Recurrence):
        self.day = day
        self.streak = session.streak
        __date = session.first_occurrence

        self.start = self.str_to_datetime(start, day, session_start=__date)
        self.end = self.str_to_datetime(end, day, session_start=__date)

    @classmethod
    def today(cls) -> Day:
        return Day(datetime.today().weekday())

    @classmethod
    def str_to_datetime(cls, t: str, day: Day, session_start: datetime) -> datetime:
        weekday_diff = (day.value - session_start.weekday() + 7) % 7
        target_date = session_start + timedelta(days=weekday_diff)
        return datetime.combine(
            target_date.date(), datetime.strptime(t, "%H:%M").time()
        )
