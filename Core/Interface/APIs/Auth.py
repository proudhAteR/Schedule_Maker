from abc import ABC, abstractmethod


class Auth(ABC):

    @abstractmethod
    def run(self):
        pass
