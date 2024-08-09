from entities.court import Court
from dataclasses import dataclass
import json

@dataclass
class CaseType:
    code: int
    """The code of the case type."""

    description: str
    """The description of the case type."""

    court: Court
    """The court associated with the case type."""

    def json(self):
        return {
            "code": self.code,
            "description": self.description,
            "court_state_code": self.court.state_code,
            "court_court_code": self.court.court_code,
        }
