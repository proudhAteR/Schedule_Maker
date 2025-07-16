from dataclasses import dataclass
from datetime import datetime


@dataclass
class Recurrence:
    first_occurrence: datetime = datetime.now()
    streak: int = 15
