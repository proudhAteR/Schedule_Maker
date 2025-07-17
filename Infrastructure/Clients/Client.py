from abc import ABC

from requests import Session, Request


class Client(ABC):
    def __init__(self, request: Session | Request | None = None):
        self.request = request or Session()
