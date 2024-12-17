from dataclasses import dataclass
from datetime import datetime


@dataclass
class CauseList:
    date: datetime.date
    """Date of the Cause List"""

    filename: str
    """The filename of the cause list"""

    bench: str
    """ The name of the bench, typically the judge"""

    type: str
    """ Cause List Type, typically the cause list number or Video Conferencing"""

    eliminated: bool
    """ Whether this cause list was eliminated"""

    bench_id: str

    """ ID of the bench """
    causelist_id: str
    """ Cause list ID, not a stable identifier """

    video_conferencing: bool = False

    """ Whether this cause list is for video conferencing"""

    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%Y-%m-%d")

        if isinstance(self.eliminated, str):
            self.eliminated = self.eliminated.strip() == "Y"

        if isinstance(self.date, datetime):
            self.date = self.date.date()

        if "VIDEO CONFERENCING" in self.type.upper():
            self.video_conferencing = True
        else:
            self.video_conferencing = False

    def url(self):
        return f"https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/display_causelist.php?filename={self.filename}"

    def printable_dict(self):
        return {
            "bench": self.bench,
            "type": self.type,
        }
