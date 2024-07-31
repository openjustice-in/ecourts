from entities.court import Court
from dataclasses import dataclass


@dataclass
class CaseType:
    code: int
    description: str
    court: Court
