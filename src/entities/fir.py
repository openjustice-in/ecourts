from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FIR:
    state: str
    district: str
    police_station: str
    number: str
    year: int

    def __post_init__(self):
        if isinstance(self.year, str) and len(self.year) == 4:
            self.year = int(self.year)
        if not isinstance(self.year, int):
            self.year = None
