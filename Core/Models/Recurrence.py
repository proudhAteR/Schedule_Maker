from dataclasses import dataclass
from datetime import datetime


@dataclass
class Recurrence:
    first_occurrence: datetime
    streak: int = 15
