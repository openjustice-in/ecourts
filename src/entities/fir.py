from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FIR:
    state: str
    """The state where the FIR was filed."""

    district: str
    """The district where the FIR was filed."""

    police_station: str
    """The police station where the FIR was filed."""

    number: str
    """The FIR number."""

    year: int
    """The year the FIR was filed."""

    def __post_init__(self):
        if isinstance(self.year, str) and len(self.year) == 4:
            self.year = int(self.year)
        if not isinstance(self.year, int):
            self.year = None
