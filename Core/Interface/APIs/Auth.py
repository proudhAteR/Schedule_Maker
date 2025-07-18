from abc import ABC, abstractmethod


class Auth(ABC):

    @abstractmethod
    def auth(self):
        pass
