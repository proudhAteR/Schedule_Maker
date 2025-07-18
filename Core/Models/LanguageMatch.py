from dataclasses import dataclass
from datetime import datetime

@dataclass
class LanguageMatch :
    name : str
    location : str
    start : datetime
    end : datetime
    day_str : str
    more : str