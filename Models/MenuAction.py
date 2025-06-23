from typing import Callable


class MenuAction:
    def __init__(self, name: str, action: Callable[[], None]):
        self.name = name
        self.action = action

    def exec(self):
        return self.action()

    def display(self, index: int):
        print(f"{index}.{self.name}")
