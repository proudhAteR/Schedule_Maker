from Models.Events.Class import Class
from Models.Enum.Priority import Priority
from Models.Events.Event import Event
from Models.Recurrence import Recurrence


class EventService:
    @classmethod
    def __parse_event(cls, sentence: str, recurrence: Recurrence | None) -> Event:
        if 'by' in sentence:
            return Class.from_sentence(sentence, recurrence)

        return Event.from_sentence(sentence, recurrence)

    @classmethod
    def create_event(cls, sentence: str, priority: str = "casual", recurrence: Recurrence | None = None) -> Event:
        event: Event = cls.__parse_event(sentence, recurrence)
        event.color = Priority.from_str(priority)

        return event
