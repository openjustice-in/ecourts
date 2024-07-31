from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from parsers.utils import parse_date
from urllib.parse import urlencode

@dataclass
class Court:
    # This is same as the data in courts.csv
    __ALL_COURTS__ =  [
        ["1",None],
        ["1","2"],
        ["1","3"],
        ["1","4"],
        ["1","5"],
        ["1","6"],
        ["10",None],
        ["10","2"],
        ["11",None],
        ["12",None],
        ["12","2"],
        ["13",None],
        ["13","2"],
        ["15",None],
        ["16",None],
        ["16","2"],
        ["16","3"],
        ["16","4"],
        ["17",None],
        ["18",None],
        ["2",None],
        ["20",None],
        ["21",None],
        ["24",None],
        ["25",None],
        ["29",None],
        ["3",None],
        ["3","2"],
        ["3","3"],
        ["4",None],
        ["5",None],
        ["6",None],
        ["6","2"],
        ["6","3"],
        ["6","4"],
        ["7",None],
        ["8",None],
        ["9",None],
        ["9","2"],
    ]
    state_code: str
    district_code: str = "1"
    court_code: Optional[str] = None

    # These two are part of presentation links, but unused otherwise
    state_name: Optional[str] = None
    name: Optional[str] = None

    def __post_init__(self):
        """
        Raise an error if the court is not valid
        """
        if [self.state_code, self.court_code] not in Court.__ALL_COURTS__:
            raise ValueError("Invalid court")

    @classmethod
    def enumerate(cls):
        for c in cls.__ALL_COURTS__:
            yield Court(
                state_code = c[0],
                court_code = c[1],
                state_name = None,
                name = None

            )

    def queryParams(self):
        r = {
            "state_code": self.state_code,
            "dist_code": self.district_code
        }
        if self.court_code:
            r["court_code"] = self.court_code
        return r

@dataclass
class Order:
    filename: str
    case_number: str
    cino: str
    court: Court

    judge: Optional[str] = ""
    date: Optional[datetime.date] = None
    appFlag: Optional[str] = ""
    judgement = Optional[bool]

    def pdf_url(self):
        if self.filename:
            return f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/display_pdf.php?{urlencode(self.queryParams())}"
    
    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = parse_date(self.date)

    def queryParams(self):
        return {
            "filename": self.filename,
            "caseno": self.case_number,
            "cCode": self.court.court_code,
            "appFlag": self.appFlag,
            "cino": self.cino,
            "state_code": self.court.state_code,
        }


@dataclass
class Party:
    name: str

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


@dataclass
class Objection:
    scrutiny_date: Optional[datetime.date]
    objection: str
    compliance_date: Optional[datetime.date]
    receipt_date: Optional[datetime.date]

    def __post_init__(self):
        if isinstance(self.scrutiny_date, str):
            self.scrutiny_date = parse_date(self.scrutiny_date)
        if isinstance(self.compliance_date, str):
            self.compliance_date = parse_date(self.compliance_date)
        if isinstance(self.receipt_date, str):
            self.receipt_date = parse_date(self.receipt_date)

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

@dataclass
class CaseType:
    code: int
    description: str
    court: Court
