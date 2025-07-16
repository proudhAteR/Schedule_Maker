import inspect

from Core.Interface.Parser import Parser
from Core.Models.Enum.Day import Day
from Core.Models.Events.Event import Event

from Core.Models.Period import Period
from Core.Models.Recurrence import Recurrence
from Infrastructure.Utils.LanguageHandler import LanguageHandler


class EventParser(Parser):
    def __init__(self):
        self.language = LanguageHandler()

    def parse(self, sentence: str, recurrence: Recurrence | None = None) -> Event:
        name, location, start, end, day_str, more = self.language.pattern_match(sentence)
        day, recurrence = self.__recurrence_gestion(day_str, recurrence)
        period = Period(start, end, day, recurrence)

        event = Event.detect_type(sentence)

        kwargs = {
            'name': name.strip(),
            'period': period,
            'location': location.strip(),
        }

        kwargs = self.__define_args(kwargs, event, more)

        # noinspection PyArgumentList
        return event(**kwargs)

    @staticmethod
    def __define_args(kwargs: dict, event: type['Event'], more: str):
        sig = inspect.signature(event.__init__)
        valid_keys = set(p for p in sig.parameters if p != "self")

        filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_keys}
        extra_keys = valid_keys - set(filtered_kwargs.keys())

        if more.strip() and extra_keys:
            filtered_kwargs[next(iter(extra_keys))] = more.strip()

        return filtered_kwargs

    @staticmethod
    def __recurrence_gestion(day_str: str | None, recurrence: Recurrence | None) -> tuple:
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
