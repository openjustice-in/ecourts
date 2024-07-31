from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Court:
    # This is same as the data in courts.csv
    __ALL_COURTS__ = [
        ["1", None],
        ["1", "2"],
        ["1", "3"],
        ["1", "4"],
        ["1", "5"],
        ["1", "6"],
        ["2", None],
        ["3", None],
        ["3", "2"],
        ["3", "3"],
        ["4", None],
        ["5", None],
        ["6", None],
        ["6", "2"],
        ["6", "3"],
        ["6", "4"],
        ["7", None],
        ["8", None],
        ["9", None],
        ["9", "2"],
        ["10", None],
        ["10", "2"],
        ["11", None],
        ["12", None],
        ["12", "2"],
        ["13", None],
        ["13", "2"],
        ["15", None],
        ["16", None],
        ["16", "2"],
        ["16", "3"],
        ["16", "4"],
        ["17", None],
        ["18", None],
        ["20", None],
        ["21", None],
        ["24", None],
        ["25", None],
        ["29", None],
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
            yield Court(state_code=c[0], court_code=c[1], state_name=None, name=None)

    def queryParams(self):
        r = {"state_code": self.state_code, "dist_code": self.district_code}
        if self.court_code:
            r["court_code"] = self.court_code
        return r
