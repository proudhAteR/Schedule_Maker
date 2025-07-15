from Models.Schedule import Schedule
from Services.APIService import APIService
from Services.EventService import EventService


class Scheduler:

    def __init__(self):
        self.api = APIService()

    async def event(self, sentence: str, priority: str):
        event = EventService.create_event(sentence, priority)
        await self.api.insert(event)

    async def schedule(self, block: list[str], session_start: str | None = None):
        await self.api.make_schedule(
            Schedule.from_block(block, session_start)
        )
