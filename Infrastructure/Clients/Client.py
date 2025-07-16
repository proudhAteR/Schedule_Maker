from requests import Session, Request


class Client:
    def __init__(self, base_url: str, request: Session | Request | None = None):
        self.base_url = base_url
        self.request = request or Session()
