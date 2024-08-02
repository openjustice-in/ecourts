from dataclasses import dataclass
from datetime import datetime
from parsers.utils import parse_date
from entities import Court


@dataclass
class Business:
    """
    A business entity is a dated interaction
    between the court and a given case
    """
    court: Court
    """The court where the business happened"""

    next_date: datetime.date
    """Date of scheduled next hearing"""

    case_number: str
    """The case number"""

    disposal_flag: str
    """case disposal status as of this business"""

    business_date: datetime.date
    """The date of the business."""

    court_number: str
    """
    The court number used to fetch the business details.
    This is different from a court code, and is typically a 4 digit number
    """

    srno: str
    """The serial number of the business."""

    def __post_init__(self):
        """
        Post-initialization processing to parse date strings and convert srno to int.
        """
        if isinstance(self.next_date, str) and len(self.next_date) < 15:
            self.next_date = parse_date(self.next_date)
        if isinstance(self.business_date, str):
            self.business_date = parse_date(self.business_date)
        if len(self.srno) > 0:
            self.srno = int(self.srno)

    def expandParams(self):
        """
        Expand the parameters into a dictionary format
        that can be used to fetch more details in HTML
        format

        Returns:
            dict: A dictionary containing the expanded parameters.
        """
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
