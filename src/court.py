from dataclasses import dataclass

@dataclass
class Court:
     state_cd: int
     dist_cd: int
     court_code: int
     stateNm: str
     name: str