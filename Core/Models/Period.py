from datetime import datetime

from Core.Models.Recurrence import Recurrence
from Core.Models.Enum.Day import Day


class Period:
    def __init__(self, start: datetime, end: datetime, day: Day, session: Recurrence):
        self.day = day
        self.streak = session.streak
        __date = session.first_occurrence

        self.start = start
        self.end = end

    @classmethod
    def today(cls) -> Day:
        return Day(datetime.today().weekday())
