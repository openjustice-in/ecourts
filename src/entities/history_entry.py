from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from parsers.utils import parse_date
from entities.business import Business


@dataclass
class HistoryEntry:
    cause_list_type: str
    judge: str
    business_on_date: Optional[datetime.date]
    hearing_date: Optional[datetime.date]
    purpose_of_hearing: str
    business: Optional[Business]

    def __post_init__(self):
        if isinstance(self.business_on_date, str):
            self.business_on_date = parse_date(self.business_on_date)
        if isinstance(self.hearing_date, str):
            self.hearing_date = parse_date(self.hearing_date)
