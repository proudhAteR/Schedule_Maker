import inspect
from datetime import datetime

from Core.Interface.Parser import Parser
from Core.Models.Events.Event import Event
from Core.Models.Time.Period import Period
from Core.Models.Time.Recurrence import Recurrence
from Infrastructure.Services.Language.LanguageService import LanguageService
from Infrastructure.Utils.Parser.TimeParser import TimeParser


class EventParser(Parser):
    def __init__(self, language_service: LanguageService = None):
        self._language = language_service or LanguageService()

    async def parse(self, sentence: str, recurrence: Recurrence = None) -> Event:
        match = await self._language.match(sentence)
        period = Period.from_match(match, recurrence)
        event_cls = Event.detect_type(match.title)

        kwargs = self._prepare_event_kwargs(match.title, period, match.location, event_cls, match.extra)

        return event_cls(**kwargs)

    def _prepare_event_kwargs(self, title: str, period: Period, location: str, event_cls: type[Event],
                              extra: str) -> dict:
        base_kwargs = {
            'name': title,
            'period': period,
            'location': location,
        }
        return self._filter_kwargs(base_kwargs, event_cls, extra)

    @staticmethod
    def _filter_kwargs(kwargs: dict, event_cls: type[Event], extra: str | None) -> dict:
        sig = inspect.signature(event_cls.__init__)
        param_names = [p for p in sig.parameters if p != "self"]
        filtered = {k: v for k, v in kwargs.items() if k in param_names}

        EventParser._fill_kwargs(param_names, filtered, extra)
        return filtered

    @staticmethod
    def _fill_kwargs(param_names: list[str], filtered: dict, extra: str | None) -> None:
        extra_value = (extra or "").strip()
        if not extra_value:
            return

        for param in param_names:
            if param not in filtered:
                filtered[param] = extra_value
                break

    async def get_date(self, date_str: str) -> datetime:
        return await self._language.parse_datetime(date_str)

    async def midnight(self, date_str: str) -> datetime:
        date = await self.get_date(date_str)
        return TimeParser.midnight(date)

    @staticmethod
    async def convert_time(event_data: dict) -> str:
        return await TimeParser.convert_time(event_data)