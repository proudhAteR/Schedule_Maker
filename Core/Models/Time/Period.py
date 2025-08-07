from datetime import datetime

from Core.Models.Enum.Day import Day
from Core.Models.Match import Match
from Core.Models.Time.Recurrence import Recurrence


class Period:
    def __init__(self, start: datetime, end: datetime, day: str | Day | None, recurrence: Recurrence):
        self.day = self.__parse_day(day)
        self.start = start
        self.end = end
        self.streak = recurrence.streak

    @classmethod
    def from_match(cls, match: Match, recurrence: Recurrence | None) -> "Period":
        recurrence = Recurrence.update_from(recurrence, match.day_str)
        return cls(match.start, match.end, match.day_str, recurrence)

    def __parse_day(self, day_input: str | Day | None) -> Day:
        if isinstance(day_input, Day):
            return day_input

        if isinstance(day_input, str) and day_input.strip():
            try:
                return Day[day_input.strip().upper()]
            except KeyError:
                raise ValueError(f"Unknown day: {day_input}")

        return self.__today()

    @staticmethod
    def __today() -> Day:
        return Day(datetime.today().weekday())
