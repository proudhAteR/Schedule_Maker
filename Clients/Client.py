import requests
from requests import *


class Client:

    def __init__(self, scope: str):
        self.scope = scope

    def get(self, endpoint: str) -> Response:
        response = requests.get(self.scope + endpoint)

        if response.status_code != 200:
            raise RuntimeError(f"Error fetching data: {response.status_code}")

        return response

    def post(self, endpoint: str) -> Response:
        return requests.post(self.scope + endpoint)
