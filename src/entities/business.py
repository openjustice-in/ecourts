from dataclasses import dataclass
from datetime import datetime
from parsers.utils import parse_date

@dataclass
class Business:
    court_code: str
    dist_code: str
    nextdate1: datetime.date
    case_number1: str
    state_code: str
    disposal_flag: str
    businessDate: datetime.date
    court_no: str
    srno: str

    def __post_init__(self):
        if isinstance(self.nextdate1, str):
            self.nextdate1 = parse_date(self.nextdate1)
        if isinstance(self.businessDate, str):
            self.businessDate = parse_date(self.businessDate)