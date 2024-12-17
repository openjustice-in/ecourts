from dataclasses import dataclass
from entities.court import Court
from typing import Optional
from parsers.utils import parse_date
import datetime
from urllib.parse import urlencode


@dataclass
class Order:
    filename: str
    """The filename of the order."""

    judge: Optional[str] = ""
    """The judge associated with the order."""

    date: Optional[datetime.date] = None
    """The date of the order."""

    judgement: Optional[bool] = None
    """Indicates if the order is a judgement."""

    def __post_init__(self):
        """
        Post-initialization processing to parse date strings and clean case number.
        """
        if isinstance(self.date, str):
            self.date = parse_date(self.date)
