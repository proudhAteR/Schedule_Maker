from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    first_occurrence: datetime
    streak: int = 15
