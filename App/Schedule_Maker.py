from Models.Class import Class
from Models.Schedule import Schedule
from Services.APIService import APIService


class Scheduler:

    def __init__(self):
        self.service = APIService()

    def event(self, sentence: str):
        event = Class.from_sentence(sentence)
        self.service.create_event(event)

    def schedule(self, block: str, session_start: str | None = None):
        self.service.make_schedule(
            Schedule.from_block(block, session_start)
        )
