from dataclasses import dataclass

@dataclass
class Position:
    hor: float
    vert: float

    def __iter__(self):
        yield self.hor
        yield self.vert