from dataclasses import dataclass
from typing import Optional

@dataclass
class Party:
    name: str
    """The name of the party."""

    advocate: Optional[str] = None
    """The advocate representing the party, if any."""
