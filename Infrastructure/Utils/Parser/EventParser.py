import inspect

from Core.Interface.Parser import Parser
from Core.Models.Events.Event import Event
from Core.Models.Time.Period import Period
from Core.Models.Time.Recurrence import Recurrence
from Infrastructure.Services.LanguageService import LanguageService


class EventParser(Parser):
    def __init__(self):
        self.__language = LanguageService()

    async def parse(self, sentence: str, recurrence: Recurrence | None = None) -> Event:
        match = await self.__language.match(sentence)
        period = Period.from_match(match, recurrence)
        event = Event.detect_type(match.title)

        kwargs = {
            'name': match.title,
            'period': period,
            'location': match.location,
        }

        kwargs = self.__define_args(kwargs, event, match.extra)

        # noinspection PyArgumentList
        return event(**kwargs)

    @staticmethod
    def __define_args(kwargs: dict, event: type['Event'], extra: str):
        sig = inspect.signature(event.__init__)
        param_names = [p for p in sig.parameters if p != "self"]
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in param_names}

        for param in param_names:
            if param not in filtered_kwargs:
                if extra.strip():
                    filtered_kwargs[param] = extra.strip()
                break

        return filtered_kwargs

    async def get_date(self, date_str: str):
        return await self.__language.parse_datetime(date_str)
