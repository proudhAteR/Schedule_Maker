from Models.Class import Class
from Models.Schedule import Schedule
from Services.APIService import APIService
from Utils.Scheduler_Utils import *


class Scheduler:

    def __init__(self):
        self.service = APIService()

    def event(self, sentence: str):
        sentence_instructions()
        event = Class.from_sentence(sentence)
        self.service.create_event(event)

    def schedule(self, block: str):
        sentence_instructions()
        block_instructions()
        self.service.make_schedule(
            Schedule.from_block(block.strip().split())
        )
