from datetime import datetime, time
from Models.enum import Day


def _str_to_time(t: str) -> time:
    return datetime.strptime(t, "%H:%M").time()


class Period:
    def __init__(self, start: str, end: str, day: Day):
        self.start: time = _str_to_time(start)
        self.end: time = _str_to_time(end)
        self.day: Day = day