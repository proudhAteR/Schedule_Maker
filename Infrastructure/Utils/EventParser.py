import re

from Core.Interface.Parser import Parser
from Core.Models.Enum.Day import Day
from Core.Models.Events.Class import Class
from Core.Models.Events.Event import Event
from Core.Models.Period import Period
from Core.Models.Recurrence import Recurrence


class EventParser(Parser):

    def parse(self, sentence: str, recurrence: Recurrence | None = None) -> Event:
        is_class = 'by' in sentence.lower()
        name, location, start, end, day_str, teacher = self.__pattern_match(sentence)
        day, recurrence = self.__recurrence_gestion(day_str, recurrence)
        period = Period(
            start.strip(),
            end.strip(),
            day,
            recurrence
        )

        if not is_class:
            return Event(
                name.strip(), period, location.strip()
            )

        return Class(
            name.strip(), period, location.strip(), teacher
        )

    @classmethod
    def __pattern_match(cls, sentence: str) -> tuple:
        pattern = r"^(.*?) in (.*?) from (.*?) to (.*?)(?: every (.*?))?(?: by (.*))?$"
        match = re.match(pattern, sentence.strip())

        if not match:
            raise ValueError("Sentence format invalid.")

        return tuple(part or "" for part in match.groups())

    @classmethod
    def __recurrence_gestion(cls, day_str: str | None, recurrence: Recurrence | None) -> tuple:
        recurrence = recurrence or Recurrence()
        day = Period.today()

        if not day_str:
            return day, Recurrence(streak=1)

        try:
            day = Day[
                day_str.strip().upper()
            ]
        except KeyError:
            raise ValueError(f"Unknown day: {day_str}")

        return day, recurrence
