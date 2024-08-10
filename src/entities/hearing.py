from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict
from parsers.utils import parse_date

class UnexpandableHearing(Exception):
    pass

@dataclass
class Hearing:
    cause_list_type: Optional[str] = None
    """The type of cause list."""

    judge: Optional[str] = None
    """The judge associated with the hearing."""

    purpose: Optional[str] = None
    """The purpose of the hearing."""

    details: Optional[Dict[str, str]] = None
    """Additional details as a dict"""

    date: Optional[datetime.date] = None
    """The date of the case hearing."""

    next_date: Optional[datetime.date] = None
    """The date of the next scheduled hearing."""

    court_no: Optional[str] = None
    """4 digit court number,which can differ between hearings"""
    
    srno: Optional[int] = None
    """2-3 digit serial number for this hearing within the case"""

    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = parse_date(self.date[0:10])
        if isinstance(self.next_date, str):
            self.next_date = parse_date(self.next_date[0:10])
        if isinstance(self.srno, str):
            self.srno = int(self.srno)

    # Additional params required
    # caseNumber1: CASE_No
    # state_code, dist_code, court_code(If present)
    def expandParams(self):
        return {
            "court_no": self.court_no,
            "businessDate": self.date.strftime("%d-%m-%Y"),
            "srno": self.srno,
        }
