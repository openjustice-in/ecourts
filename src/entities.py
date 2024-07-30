from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from ecourts.parsers.utils import parse_date


@dataclass
class Party:
    name: str


@dataclass
class Order:
    caseno: str
    judge: str
    date: datetime.date
    filename: Optional[str]
    cCode: Optional[str]
    cino: Optional[str]
    state_code: Optional[str]
    appFlag: Optional[str] = ""

    def pdf_url():
        if self.filename:
            return f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/display_pdf.php?filename={filename}&caseno={caseno}&cCode={cCode}&appFlag={appFlag}&cino={cino}&state_code={state_code}"
        return None


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
        if self.nextdate1 instanceof str:
            self.nextdate1 = parse_date(self.nextdate1)
        if self.businessDate instanceof str:
            self.businessDate = parse_date(self.businessDate)


@dataclass
class HistoryEntry:
    cause_list_type: str
    judge: str
    business_on_date: Optional[datetime.date]
    hearing_date: Optional[datetime.date]
    purpose_of_hearing: str
    business: Optional[Business]


@dataclass
class Objection:
    scrutiny_date: Optional[datetime.date]
    objection: str
    compliance_date: Optional[datetime.date]
    receipt_date: Optional[datetime.date]


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

@dataclass
class Court:
    state_cd: str
    dist_cd: str
    court_code: str
    stateNm: str
    name: str
