from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from parsers.utils import parse_date
from entities.business import Business


@dataclass
class HistoryEntry:
    cause_list_type: str
    """The type of cause list."""

    judge: str
    """The judge associated with the history entry."""

    business_on_date: Optional[datetime.date]
    """The date of the business."""

    hearing_date: Optional[datetime.date]
    """The date of the hearing."""

    purpose_of_hearing: str
    """The purpose of the hearing."""

    business: Optional[Business]
    """The business details associated with the history entry."""

    def __post_init__(self):
        if isinstance(self.business_on_date, str):
            self.business_on_date = parse_date(self.business_on_date)
        if isinstance(self.hearing_date, str):
            self.hearing_date = parse_date(self.hearing_date)
