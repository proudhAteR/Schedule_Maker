from requests import Session, Request


class Client:
    def __init__(self, request: Session | Request | None = None):
        self.request = request or Session()
