from abc import abstractmethod, ABC


class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, sentence : str):
        pass
