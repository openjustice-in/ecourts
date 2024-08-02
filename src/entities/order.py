from dataclasses import dataclass
from entities.court import Court
from typing import List, Dict, Optional
from parsers.utils import parse_date
import datetime
from urllib.parse import urlencode


@dataclass
class Order:
    filename: str
    """The filename of the order."""

    case_number: str
    """The case number associated with the order."""

    cino: str
    """The CINO (Case Identification Number) of the order."""

    court: Court
    """The court associated with the order."""

    judge: Optional[str] = ""
    """The judge associated with the order."""

    date: Optional[datetime.date] = None
    """The date of the order."""

    appFlag: Optional[str] = ""
    """The application flag of the order."""

    judgement: Optional[bool] = None
    """Indicates if the order is a judgement."""

    def pdf_url(self):
        """
        Generate the URL to access the PDF of the order.

        Returns:
            str: The URL to access the PDF of the order.
        """
        if self.filename:
            return f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/display_pdf.php?{urlencode(self.queryParams())}"

    def __post_init__(self):
        """
        Post-initialization processing to parse date strings and clean case number.
        """
        if isinstance(self.date, str):
            self.date = parse_date(self.date)
        self.case_number = self.case_number.replace("\ufeff", "")

    def queryParams(self):
        """
        Generate query parameters for the order.

        Returns:
            dict: A dictionary containing the query parameters.
        """
        return {
            "filename": self.filename,
            "caseno": self.case_number,
            "cCode": self.court.court_code,
            "appFlag": self.appFlag,
            "cino": self.cino,
            "state_code": self.court.state_code,
        }
