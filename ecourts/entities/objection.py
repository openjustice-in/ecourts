from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from parsers.utils import parse_date


@dataclass
class Objection:
    scrutiny_date: Optional[datetime.date]
    """The date of scrutiny."""

    objection: str
    """The objection text."""

    compliance_date: Optional[datetime.date]
    """The date of compliance."""

    receipt_date: Optional[datetime.date]
    """The date of receipt."""

    def __post_init__(self):
        if isinstance(self.scrutiny_date, str):
            self.scrutiny_date = parse_date(self.scrutiny_date)
        if isinstance(self.compliance_date, str):
            self.compliance_date = parse_date(self.compliance_date)
        if isinstance(self.receipt_date, str):
            self.receipt_date = parse_date(self.receipt_date)
