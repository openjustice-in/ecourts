from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from parsers.utils import parse_date
from entities.court import Court
from entities.history_entry import HistoryEntry
from entities.party import Party
from entities.order import Order
from entities.fir import FIR
from entities.objection import Objection


@dataclass
class Case:
    case_type: str
    registration_number: str
    cnr_number: str
    filing_number: Optional[str] = None

    registration_date: Optional[datetime.date] = None
    first_hearing_date: Optional[datetime.date] = None
    decision_date: Optional[datetime.date] = None
    case_status: Optional[str] = None
    nature_of_disposal: Optional[str] = None
    coram: Optional[str] = None
    bench: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    judicial: Optional[str] = None
    petitioners: Optional[List[Party]] = None
    respondents: Optional[List[Party]] = None
    orders: Optional[List[Order]] = None

    history: Optional[List[HistoryEntry]] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    objections: Optional[List[Objection]] = None
    not_before_me: Optional[str] = None
    filing_date: Optional[datetime.date] = None
    fir: Optional[FIR] = None

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
