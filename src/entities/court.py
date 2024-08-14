from dataclasses import dataclass
from typing import Optional
import json


@dataclass
class Court:
    """
    Represents a court entity with state, district, and court codes.
    """

    # This is same as the data in courts.csv
    __ALL_COURTS__ = [
        ("1", None),
        ("1", "2"),
        ("1", "3"),
        ("1", "4"),
        ("1", "5"),
        ("1", "6"),
        ("2", None),
        ("3", None),
        ("3", "2"),
        ("3", "3"),
        ("4", None),
        ("5", None),
        ("6", None),
        ("6", "2"),
        ("6", "3"),
        ("6", "4"),
        ("7", None),
        ("8", None),
        ("9", None),
        ("9", "2"),
        ("10", None),
        ("10", "2"),
        ("11", None),
        ("12", None),
        ("12", "2"),
        ("13", None),
        ("13", "2"),
        ("15", None),
        ("16", None),
        ("16", "2"),
        ("16", "3"),
        ("16", "4"),
        ("17", None),
        ("18", None),
        ("20", None),
        ("21", None),
        ("24", None),
        ("25", None),
        ("29", None),
    ]
    state_code: str
    """The state code of the court."""

    district_code: str = "1"
    """The district code of the court."""

    court_code: Optional[str] = None
    """The court code, if applicable."""

    # These two are part of presentation links, but unused otherwise
    state_name: Optional[str] = None
    """The name of the state, if available."""

    name: Optional[str] = None
    """The name of the court, if available."""

    def __post_init__(self):
        """
        Post-initialization processing to validate the court.
        """
        """
        Raise an error if the court is not valid
        """
        lcc = self.court_code
        if self.court_code == "1":
            lcc = None
        if (self.state_code,  lcc) not in Court.__ALL_COURTS__:
            if self.court_code:
                raise ValueError(
                    f"Invalid court: state_code={self.state_code}, court_code={self.court_code}"
                )
            else:
                raise ValueError(f"Invalid court: state_code={self.state_code}")

        if self.district_code == None:
            self.district_code = "1"

    @classmethod
    def enumerate(cls):
        """
        Enumerate all known valid courts.

        Yields:
            Court: A court object for each valid court.
        """
        for c in cls.__ALL_COURTS__:
            yield Court(state_code=c[0], court_code=c[1], state_name=None, name=None)

    def queryParams(self):
        """
        Generate query parameters for the court.

        Returns:
            dict: A dictionary containing the query parameters.
        """
        r = {"state_code": self.state_code, "dist_code": self.district_code}
        
        r["court_code"] = self.court_code or "1"
        return r

    def json(self):
        """
        Generate a JSON representation of the court.

        Returns:
            dict: A dictionary containing the JSON representation.
        """
        return {
            "state_code": self.state_code,
            "district_code": self.district_code,
            "court_code": self.court_code,
        }

    def __iter__(self):
        for key in ["state_code", "district_code", "court_code"]:
            yield key, getattr(self, key)
