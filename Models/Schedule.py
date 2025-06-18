from Models.Class import Class
from Models.Event import Event
from Services.Logger import get_logger


class Schedule:
    def __init__(self, events: list[Event]):
        self.events = events

    @classmethod
    def from_block(cls, block: list[str]) -> 'Schedule':
        events = []

        for line in block:
            try:
                event = Class.from_sentence(line)
                events.append(event)
            except Exception as e:
                get_logger().error(f"Failed to parse line: '{line}'. Reason: {e}")

        return Schedule(events)
