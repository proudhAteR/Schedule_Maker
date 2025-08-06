from dataclasses import dataclass
from datetime import datetime

@dataclass
class LanguageMatch :
    title : str
    location : str
    start : datetime
    end : datetime
    day_str : str
    extra : str