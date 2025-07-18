from abc import ABC, abstractmethod
from Infrastructure.Clients.Client import Client
from typing import TypeVar, Generic

TClient = TypeVar("TClient", bound=Client)


class API(Generic[TClient], ABC):

    @abstractmethod
    def __init__(self, client: TClient = Client()):
        self.client = client
