from Models.menu import Menu
from Models.menu_action import MenuAction


def display_title():
    print(r"""
███████╗ ██████╗██╗  ██╗███████╗██████╗ ██╗   ██╗██╗     ███████╗██████╗ 
██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗██║   ██║██║     ██╔════╝██╔══██╗
███████╗██║     ███████║█████╗  ██║  ██║██║   ██║██║     █████╗  ██████╔╝
╚════██║██║     ██╔══██║██╔══╝  ██║  ██║██║   ██║██║     ██╔══╝  ██╔══██╗
███████║╚██████╗██║  ██║███████╗██████╔╝╚██████╔╝███████╗███████╗██║  ██║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝""")


class Scheduler:

    def __init__(self):
        self.menu: Menu = Menu([
            MenuAction("Make schedule", lambda: None),
            MenuAction("Create event", lambda: None)
        ])

    def run(self):
        display_title()
        self.display_menu()

    def display_menu(self):
        while True:
            self.show_options()
            if self.handle_choice():
                return

    def show_options(self):
        print("\nSelect an option:")
        for i, action in enumerate(self.menu.actions):
            action.display(i)

    def handle_choice(self) -> bool:
        try:
            choice = int(input("\nEnter the number of your choice: ")) - 1
            if self.is_valid_choice(choice):
                print()
                selection = self.menu.actions[choice]
                selection.action()

                return selection.name.lower() == 'quit'

            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
        return False

    def is_valid_choice(self, choice):
        return 0 <= choice < len(self.menu.actions)
