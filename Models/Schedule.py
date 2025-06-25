import re
from datetime import datetime

from Models.Class import Class
from Models.Event import Event
from Models.Session import Session
from Utils.Logger import Logger


class Schedule:
    def __init__(self, events: list[Event], schedule_session: Session | None = None):
        self.events = events
        self.session = schedule_session

    @classmethod
    def from_block(cls, block: list[str]) -> 'Schedule':
        events = []
        schedule_session = None
        pattern = r"Schedule starts on\s+(\d{4}-\d{2}-\d{2})"
        match = re.match(pattern, block[0])
        if match:
            date_str = match.group(1)
            schedule_session = Session(first_occurrence=datetime.strptime(date_str, "%Y-%m-%d"))
            block = block[1:]

        for line in block:
            try:
                event = Class.from_sentence(line, schedule_session)
                events.append(event)
            except Exception as e:
                Logger().logger.error(f"Failed to parse line: '{line}'. Reason: {e}")

        return Schedule(events, schedule_session)
