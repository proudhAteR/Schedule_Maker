from Models.menu_action import MenuAction


class Menu:
    def __init__(self, actions: list[MenuAction]):
        self.actions = actions

    def is_valid_choice(self, choice):
        return 0 <= choice < len(self.actions)
