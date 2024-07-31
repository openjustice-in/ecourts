from dataclasses import dataclass
from entities.court import Court
from typing import List, Dict, Optional
from parsers.utils import parse_date
import datetime
from urllib.parse import urlencode

@dataclass
class Order:
    filename: str
    case_number: str
    cino: str
    court: Court

    judge: Optional[str] = ""
    date: Optional[datetime.date] = None
    appFlag: Optional[str] = ""
    judgement: Optional[bool] = None

    def pdf_url(self):
        if self.filename:
            return f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/display_pdf.php?{urlencode(self.queryParams())}"
    
    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = parse_date(self.date)
        self.case_number = self.case_number.replace("\ufeff", "")

    def queryParams(self):
        return {
            "filename": self.filename,
            "caseno": self.case_number,
            "cCode": self.court.court_code,
            "appFlag": self.appFlag,
            "cino": self.cino,
            "state_code": self.court.state_code,
        }
