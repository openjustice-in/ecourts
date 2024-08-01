from dataclasses import dataclass
from typing import Optional

@dataclass
class Party:
    name: str
    advocate: Optional[str] = None
