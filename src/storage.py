from entities import CaseType, Court
import sqlite3
import json


class Storage:
    """
    A class that implements storage for various dataclasses
    in a local sqlite database. The database is called
    ecourts.db in the PWD unless one is specified.

    Every dataclass is converted to a JSON object stored using the
    sqlite json extension.
    """

    def __init__(self, filename="ecourts.db"):
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS case_types (value JSON)")
        self.cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_case_types ON case_types(json_extract(value, '$.code'), json_extract(value, '$.court_state_code'), json_extract(value, '$.court_court_code'))"
        )
        self.cursor.execute("CREATE TABLE IF NOT EXISTS courts (value JSON)")
        self.conn.commit()

    def addCaseTypes(self, records: list[CaseType]):
        for record in records:
            self.cursor.execute(
                "INSERT OR IGNORE INTO case_types VALUES (?)",
                (json.dumps(dict(record)),),
            )
        self.conn.commit()

    def getCaseTypes(self):
        r = self.conn.execute("SELECT * FROM case_types")
        for record in r:
            j = json.loads(record["value"])
            court = Court(
                state_code=j["court_state_code"], court_code=j["court_court_code"]
            )
            yield CaseType(code=j["code"], description=j["description"], court=court)

    def addCourts(self, records: list[Court]):
        for record in records:
            self.cursor.execute(
                "INSERT OR IGNORE INTO courts VALUES (?)", (json.dumps(dict(record)),)
            )
        self.conn.commit()
