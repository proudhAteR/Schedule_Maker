from textwrap import dedent

from Models.Class import Class
from Models.Schedule import Schedule
from Models.menu import Menu
from Models.menu_action import MenuAction
from Services.Logger import get_logger
from Services.ScheduleService import ScheduleService


def display_title():
    print(r"""
███████╗ ██████╗██╗  ██╗███████╗██████╗ ██╗   ██╗██╗     ███████╗██████╗ 
██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔════╝██╔══██╗
███████╗██║     ███████║█████╗  ██║  ██║██║   ██║██║     █████╗  ██████╔╝
╚════██║██║     ██╔══██║██╔══╝  ██║  ██║██║   ██║██║     ██╔══╝  ██╔══██╗
███████║╚██████╗██║  ██║███████╗██████╔╝╚██████╔╝███████╗███████╗██║  ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝""")


def handle_choice(menu: Menu) -> bool:
    try:
        choice = int(input("Enter number: ")) - 1
        if menu.is_valid_choice(choice):
            print()
            selection = menu.actions[choice]
            selection.action()

            return selection.name.lower() == 'quit'

        print("Invalid choice. Please try again.")
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


def show_help():
    print("""
    ─────────────── Schedule Maker Documentation ───────────────

    This application helps you manage your class schedules via a command-line interface.

    ➤ Available Options:
    1. Make schedule – Allows you to paste multiple events at once.
    2. Create event – Enter a single event manually.

    ➤ Event Format:
    Each event must follow this format:
    [Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
    Example:
    Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith

    ➤ Schedule from Start Date (Optional):
    To specify when a schedule begins, start your input block with:
    Schedule starts on [Date]
    Example:
    Schedule starts on 2025-09-01

    ➤ Ending Input:
    When inputting multiple events, finish your block by pressing Enter twice.

    ────────────────────────────────────────────────────────────
    """)


def block_instructions():
    print(dedent("""
        [Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
        Example: Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith
    """))
    print(dedent("""
        If you want to start from a specific date you should start the schedule by:
        Schedule starts on [Date]
    """))
    print("Paste your events below (one per line). Finish input by pressing Enter twice:\n")


def sentence_instructions():
    dedent("""
        [Course Name] in [Location] from [Start Time] to [End Time] every [Day] by [Teacher]
        Example: Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith\n
    """)


class Scheduler:

    def __init__(self):
        self.service = ScheduleService()

    def run(self):
        main_menu: Menu = Menu([
            MenuAction("Make schedule", self.schedule),
            MenuAction("Create event", self.event),
            MenuAction("Help / Documentation", show_help)
        ])
        display_title()
        display_menu(main_menu)

    def event(self):
        sentence_instructions()
        sentence = input("Enter the prompt for the event creation: ")
        event = Class.from_sentence(sentence)
        self.service.create_event(event)

    def schedule(self):
        block_instructions()
        # Read multi-line block from stdin until double Enter (empty line)
        block = []
        while True:
            line = input()
            if not line.strip():
                break
            block.append(line.strip())

        if not block:
            get_logger().warning("Invalid line")
            return

        self.service.make_schedule(
            Schedule.from_block(block)
        )
