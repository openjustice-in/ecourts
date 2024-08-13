from entities.court import Court
from dataclasses import dataclass
import json


@dataclass
class ActType:
    code: int
    """The code of the act type."""

    description: str
    """The description of the act type."""

    court: Court
    """The court associated with the act type."""

    def keys(self):
        return ["code", "description", "court_state_code", "court_court_code"]

    def __getitem__(self, key):
        if key in ["code", "description"]:
            return getattr(self, key)
        elif key == "court_state_code":
            return self.court.state_code
        elif key == "court_court_code":
            return self.court.court_code
        else:
            raise KeyError(key)
