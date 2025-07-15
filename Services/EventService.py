from Models.Class import Class
from Models.Event import Event
from Models.Recurrence import Recurrence


class EventService:
    @classmethod
    def parse_event(cls, sentence: str, recurrence: Recurrence | None = None) -> Event:
        if 'by' in sentence:
            return Class.from_sentence(sentence, recurrence)

        return Event.from_sentence(sentence, recurrence)
