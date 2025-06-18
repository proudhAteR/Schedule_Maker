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


class Scheduler:

    def __init__(self):
        self.service = ScheduleService()

    def run(self):
        main_menu: Menu = Menu([
            MenuAction("Make schedule", self.schedule),
            MenuAction("Create event", self.event)
        ])
        display_title()
        display_menu(main_menu)

    def event(self):
        print("Example: Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith\n")
        sentence = input("Enter the prompt for the event creation: ")
        event = Class.from_sentence(sentence)
        self.service.create_event(event)

    def schedule(self):
        print("Paste your events below (one per line). Finish input by pressing Enter twice:\n")
        print("(Example: Math in Room 101 from 10:00 to 11:00 every Monday by Mr. Smith)\n")

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
