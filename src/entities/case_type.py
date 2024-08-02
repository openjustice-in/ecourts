from entities.court import Court
from dataclasses import dataclass


@dataclass
class CaseType:
    code: int
    """The code of the case type."""

    description: str
    """The description of the case type."""

    court: Court
    """The court associated with the case type."""
