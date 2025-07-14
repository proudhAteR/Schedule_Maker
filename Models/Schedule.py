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
    def from_block(cls, block: str, date_str: str | None = None) -> 'Schedule':
        events = []
        block_list = block.strip().split(";")
        schedule_session = None
        if date_str:
            schedule_session = Session(
                first_occurrence=datetime.strptime(date_str, "%Y-%m-%d")
            )

        for line in block_list:
            try:
                event = Class.from_sentence(line, schedule_session)
                events.append(event)
            except Exception as e:
                Logger().error(f"Failed to parse line: '{line}'. Reason: {e}")

        return Schedule(events, schedule_session)
