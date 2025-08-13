from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from Infrastructure.Clients.Client import Client

TClient = TypeVar("TClient", bound=Client)


class API(Generic[TClient], ABC):

    @abstractmethod
    def __init__(self, client: TClient = Client()):
        self.client = client
