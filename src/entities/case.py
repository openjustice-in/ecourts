from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from parsers.utils import parse_date
from entities.hearing import Hearing
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
    petitioners: Optional[list[Party]] = None
    respondents: Optional[list[Party]] = None
    orders: Optional[list[Order]] = None
    case_number: Optional[str] = None
    hearings: Optional[list[Hearing]] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    objections: Optional[list[Objection]] = None
    not_before_me: Optional[str] = None
    filing_date: Optional[datetime.date] = None
    fir: Optional[FIR] = None
    token: Optional[str] = None

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
        if self.orders == None:
            self.orders = []
        if self.hearings == None:
            self.hearings = []
        if self.objections == None:
            self.objections = []
        # The canonical representation of a CNR is without hyphens
        self.cnr_number = self.cnr_number.replace("-", "")
        if self.nature_of_disposal == "--":
            self.nature_of_disposal = None
        if len(self.cnr_number) !=16:
            raise ValueError("Invalid CNR Number")
        if self.orders == None:
            self.orders = []
        if self.hearings == None:
            self.hearings = []
        if self.objections == None:
            self.objections = []

        if self.case_number:
            assert 1990 < int(self.case_number[-4:])
            assert int(self.case_number[-4:]) < 2030


    def expandParams(self):
        if not (self.token and self.case_number):
            raise ValueError("Token/case_number not set in Case entity")
        return {
            "cino": self.cnr_number,
            "token": self.token,
            "case_no": self.case_number
        }

    def __getattribute__(self, name):
        if name == 'name':
            if len(self.petitioners) > 0 and len(self.respondents) > 0:
                return self.petitioners[0].name + " vs " + self.respondents[0].name
            else:
                return None
        else:
            return super().__getattribute__(name)

    def json(self) -> dict:
        """
        Generate a JSON representation of the Case.

        Returns:
            dict: A dictionary containing the JSON representation.
        """
        return {
            "case_type": self.case_type,
            "registration_number": self.registration_number,
            "cnr_number": self.cnr_number,
            "filing_number": self.filing_number,
            "registration_date": self.registration_date,
            "first_hearing_date": self.first_hearing_date,
            "decision_date": self.decision_date,
            "case_status": self.case_status,
            "nature_of_disposal": self.nature_of_disposal,
            "coram": self.coram,
            "bench": self.bench,
            "state": self.state,
            "district": self.district,
            "judicial": self.judicial,
            "petitioners": [asdict(p) for p in self.petitioners],
            "respondents": [asdict(r) for r in self.respondents],
            "orders": [asdict(o) for o in self.orders],
            "case_number": self.case_number,
            "hearings": [asdict(h) for h in self.hearings],
            "category": self.category,
            "sub_category": self.sub_category,
            "objections": [asdict(o) for o in self.objections],
            "not_before_me": self.not_before_me,
            "filing_date": self.filing_date,
            "fir": asdict(self.fir) if self.fir else None
        }
