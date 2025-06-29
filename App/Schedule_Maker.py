import asyncio
from textwrap import dedent

from Models.Class import Class
from Models.Schedule import Schedule
from Models.Menu import Menu
from Models.MenuAction import MenuAction
from Services.APIService import APIService
from Services.OCRService import OCRService
from Utils.Logger import Logger
from Services.OCR.TesseractOCR import TesseractOCR


def display_title():
    print(r"""
███████╗ ██████╗██╗  ██╗███████╗██████╗ ██╗   ██╗██╗     ███████╗        ███╗   ███╗ █████╗ ██╗  ██╗███████╗██████╗ 
██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔════╝        ████╗ ████║██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
███████╗██║     ███████║█████╗  ██║  ██║██║   ██║██║     █████╗          ██╔████╔██║███████║█████╔╝ █████╗  ██████╔╝
╚════██║██║     ██╔══██║██╔══╝  ██║  ██║██║   ██║██║     ██╔══╝          ██║╚██╔╝██║██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
███████║╚██████╗██║  ██║███████╗██████╔╝╚██████╔╝███████╗███████╗███████╗██║ ╚═╝ ██║██║  ██║██║  ██╗███████╗██║  ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ """)


def handle_choice(menu: Menu) -> bool:
    try:
        choice = int(input("Enter number: ")) - 1
        if menu.is_valid_choice(choice):
            print()
            selection = menu.actions[choice]
            selection.action()
            return selection.name.lower() == 'quit'
        else:
            print(f"Invalid choice: {choice + 1}. Please select a valid option.")
    except ValueError:
        print("Please enter a valid number.")
    return False


def show_options(menu: Menu):
    print("\n\nWhat would you like to do?")
    for i, action in enumerate(menu.actions, start=1):
        action.display(i)


def display_menu(menu: Menu):
    while True:
        show_options(menu)
        if handle_choice(menu):
            return


def ai_prompt():
    print(dedent("""
        I have a json file containing a class or event schedule (such as a table, timetable, or calendar view) that was transformed by an OCR process. 
        Please extract the relevant information and convert it into a list of event descriptions following this exact format:
        [Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
        
        For example:
        Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith
        
        Additional guidelines:
            - When looking for classes the hours at the levels 
            - If the schedule contains a start date (e.g., "Schedule starts on 2025-09-01"), include that line first.
            - If the schedule does not contain a start date, ask me if I want to add one.
            - Times must be in 24-hour format.
            - If the teacher’s name isn’t present, use "Unknown".
            - If the location is missing, use "TBD".
            - There shouldn't be any empty lines in the output you give me.
            - Respect the format by any means and do not change it.
            - Ignore single-letter codes like "L" and "T" as they are not days of the week or relevant information
            - You can omit activities called "Activités collège".

        Output all the extracted and formatted lines as a plain text block that I can paste directly.
    """))


def block_instructions():
    print(dedent("""
        If you want to start from a specific date, begin your schedule like this:
        Schedule starts on [Date]
    """))
    print("Paste your events below (one per line). Finish input by pressing Enter twice:\n")


def sentence_instructions():
    print(
        dedent("""
            [Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
            Example: Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith
        """)
    )


def read_block() -> list[str]:
    # Read multi-line block from stdin until double Enter (empty line)
    block = []
    while True:
        line = input()
        if not line.strip():
            break
        block.append(line.strip())

    if not block:
        Logger.warning("No input lines were provided for schedule.")

    return block


def create_event_from_sentence(sentence: str) -> Class:
    return Class.from_sentence(sentence)


def quit_app():
    print("Exiting Schedule Maker.")


class Scheduler:

    def __init__(self):
        self.schedule = APIService()

    def run(self):
        main_menu: Menu = Menu([
            MenuAction("Make schedule", self.make_schedule),
            MenuAction("Create event", self.event),
            MenuAction("Prompt", ai_prompt),
            MenuAction("Quit", quit_app)
        ])
        display_title()
        display_menu(main_menu)

    def event(self):
        sentence_instructions()
        sentence = input("Enter the prompt for the event creation: ")
        event = Class.from_sentence(sentence)
        self.schedule.create_event(event)

    def make_schedule(self):
        path = input("What is the name of the your schedule file? (e.g., schedule.jpg): ")
        try:
            service = OCRService(
                TesseractOCR(),
                debug=True
            )
            data = asyncio.run(service.extract(path))

            print(data)

            ai_prompt()
            block_instructions()
        except Exception as e:
            Logger.error(f"Cannot extract data from {path} because {e}")
            return

        block = read_block()
        self.schedule.make_schedule(
            Schedule.from_block(block)
        )
