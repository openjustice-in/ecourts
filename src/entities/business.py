from dataclasses import dataclass
from datetime import datetime
from parsers.utils import parse_date
from entities import Court

@dataclass
class Business:
    court: Court
    next_date: datetime.date
    case_number: str
    disposal_flag: str
    business_date: datetime.date
    court_number: str
    srno: str

    def __post_init__(self):
        if isinstance(self.next_date, str) and len(self.next_date)<15:
            self.next_date = parse_date(self.next_date)
        if isinstance(self.business_date, str):
            self.business_date = parse_date(self.business_date)
        if len(self.srno) > 0:
            self.srno = int(self.srno)

    def expandParams(self):
        if self.business_date:
            r = {
                "court_code": self.court.court_code,
                "dist_code": self.court.district_code,
                "state_code": self.court.state_code,
                "case_number1": self.case_number,
                "businessDate": self.business_date.strftime("%d-%m-%Y"),
                "srno": self.srno,
                "court_no": self.court_number,
                "disposal_flag": self.disposal_flag,
            }
            if self.next_date:
                r["nextDate1"] = self.next_date.strftime("%Y%m%d")
            return r
