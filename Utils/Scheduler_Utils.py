from Models.Class import Class
from Models.Menu import Menu
from textwrap import dedent

from Utils.Logger import Logger


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
