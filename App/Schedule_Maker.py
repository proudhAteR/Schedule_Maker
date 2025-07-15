from Models.Class import Class
from Models.Schedule import Schedule
from Services.APIService import APIService
from Services.EventService import EventService
from Utils.Logger import Logger


class Scheduler:

    def __init__(self):
        self.service = APIService()

    def event(self, sentence: str):
        event = EventService.parse_event(sentence)
        self.service.create_event(event)

    async def schedule(self, block: list[str], session_start: str | None = None):
        await self.service.make_schedule(
            Schedule.from_block(block, session_start)
        )
