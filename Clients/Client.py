import requests
from requests import *


class Client:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str) -> Response:
        response = requests.get(self.base_url + endpoint)

        if response.status_code != 200:
            raise RuntimeError(f"Error fetching data: {response.status_code}")

        return response

    def post(self, endpoint: str) -> Response:
        return requests.post(self.base_url + endpoint)
