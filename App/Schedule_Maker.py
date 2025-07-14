from Models.Schedule import Schedule
from Models.MenuAction import MenuAction
from Services.APIService import APIService
from Utils.Scheduler_Utils import *


class Scheduler:

    def __init__(self):
        self.service = APIService()

    def run(self):
        main_menu: Menu = Menu([
            MenuAction("Create event", self.event),
            MenuAction("Make schedule", self.schedule),
            MenuAction("Quit", quit_app)
        ])
        display_menu(main_menu)

    def event(self):
        sentence_instructions()
        sentence = input("Enter the prompt for the event creation: ")
        event = Class.from_sentence(sentence)
        self.service.create_event(event)

    def schedule(self):
        sentence_instructions()
        block_instructions()

        block = read_block()
        self.service.make_schedule(
            Schedule.from_block(block)
        )
