from Models.Schedule import Schedule
from Services.APIService import APIService
from Services.EventService import EventService
from Utils.Logger import Logger


class Scheduler:

    def __init__(self):
        self.api = APIService()

    async def event(self, sentence: str, priority: str):
        try:
            event = EventService.create_event(sentence, priority)
            await self.api.insert(event)
        except ValueError as e:
            Logger.error(f"Unable to create event. Cause: {e}")

    async def schedule(self, block: list[str], session_start: str | None = None):
        await self.api.make_schedule(
            Schedule.from_block(block, session_start)
        )
