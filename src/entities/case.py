from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from parsers.utils import parse_date
from entities.court import Court
from entities.history_entry import HistoryEntry
from entities.party import Party
from entities.order import Order
from entities.objection import Objection


@dataclass
class Case:
    case_type: str
    filing_number: str

    registration_number: str
    registration_date: Optional[datetime.date]
    cnr_number: str
    first_hearing_date: Optional[datetime.date]
    decision_date: Optional[datetime.date]
    case_status: str
    nature_of_disposal: str
    coram: Optional[str]
    bench: Optional[str]
    state: Optional[str]
    district: Optional[str]
    judicial: Optional[str]
    petitioners: Optional[List[Party]]
    respondents: Optional[List[Party]]
    orders: Optional[List[Order]]

    history: Optional[List[HistoryEntry]]
    category: Optional[str]
    sub_category: Optional[str]
    objections: Optional[List[Objection]]
    not_before_me: Optional[str]
    filing_date: Optional[datetime.date] = None

    def __post_init__(self):
        if not self.filing_date:
            self.filing_date = None
        if self.not_before_me == "":
            self.not_before_me = None
        if isinstance(self.registration_date, str):
            self.registration_date = parse_date(self.registration_date)
        if isinstance(self.first_hearing_date, str):
            self.first_hearing_date = parse_date(self.first_hearing_date)
        if isinstance(self.decision_date, str):
            self.decision_date = parse_date(self.decision_date)
        if isinstance(self.filing_date, str):
            self.filing_date = parse_date(self.filing_date)
