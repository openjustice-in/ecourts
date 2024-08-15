from entities import CaseType, Court, Case,ActType, CaseType
import sqlite3
import json
from collections.abc import Iterator


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
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS case_types (value JSON)")
        cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_case_types ON case_types(json_extract(value, '$.code'), json_extract(value, '$.court_state_code'), json_extract(value, '$.court_court_code'))"
        )

        cursor.execute("CREATE TABLE IF NOT EXISTS act_types (value JSON)")
        cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_act_types ON act_types(json_extract(value, '$.code'), json_extract(value, '$.court_state_code'), json_extract(value, '$.court_court_code'))"
        )
        cursor.execute("CREATE TABLE IF NOT EXISTS courts (value JSON)")
        cursor.execute("CREATE TABLE IF NOT EXISTS cases (state_code, court_code, value JSON)")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_cases_cnr ON cases(json_extract(value, '$.cnr_number'))")
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_cases_caseno ON cases(state_code, court_code, json_extract(value, '$.case_type'), json_extract(value, '$.registration_number'))")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cases_category ON cases(json_extract(value, '$.category'))")
        cursor.close()
        self.conn.commit()

    def close(self):
        self.conn.close()

    def addCaseTypes(self, records: list[CaseType]):
        for record in records:
            self.conn  .execute(
                "INSERT OR IGNORE INTO case_types VALUES (?)",
                (json.dumps(dict(record)),),
            )
        self.conn.commit()

    def getCaseTypes(self):
        r = self.conn.execute("SELECT value FROM case_types")
        for record in r:
            j = json.loads(record[0])
            court = Court(
                state_code=j["court_state_code"], court_code=j["court_court_code"]
            )
            yield CaseType(code=j["code"], description=j["description"], court=court)


    def addActTypes(self, records: list[ActType]):
        for record in records:
            self.conn  .execute(
                "INSERT OR IGNORE INTO act_types VALUES (?)",
                (json.dumps(dict(record)),),
            )
        self.conn.commit()

    def getActTypes(self) -> Iterator[ActType]:
        r = self.conn.execute("SELECT * FROM act_types")
        for record in r:
            j = json.loads(record[0])
            court = Court(
                state_code=j["court_state_code"], court_code=j["court_court_code"]
            )
            yield ActType(code=j["code"], description=j["description"], court=court)

    def addCourts(self, records: list[Court]):
        for record in records:
            self.conn.execute(
                "INSERT OR IGNORE INTO courts VALUES (?)", (json.dumps(dict(record)),)
            )
        self.conn.commit()

    #TODO: Move storage to under ecourts.storage so we get court information from there
    def addCases(self, court: Court, cases: list[Case], extra_fields: dict={}):
        cursor = self.conn.cursor()
        for case in cases:
            # search for the record using CNR
            # if found, update the record
            # if not found, insert the record
            search_result = cursor.execute(
                "SELECT value FROM cases WHERE json_extract(value, '$.cnr_number') = ?", (case.cnr_number,)
            ).fetchone()
            if search_result:
                existing_row = json.loads(search_result[0])
                patch = {}
                for k in ['status', 'year', 'act_type', 'case_type']:
                    patch[k] = extra_fields.get(k, existing_row.get(k))
                d = json.dumps(case.json() | patch, default=str)
                self.conn.execute("UPDATE cases SET value = ? WHERE json_extract(value, '$.cnr_number') = ?", (d, case.cnr_number))
            else:
                d = json.dumps(case.json() | extra_fields, default=str)
                cursor.execute(
                    "INSERT INTO cases VALUES (?, ?, ?)", (court.state_code, court.court_code or "1", d)
                )
        cursor.close()
        self.conn.commit()

    def getCases(self):
        for (state_code, court_code, value) in self.conn.execute("SELECT state_code, court_code, value FROM cases ORDER BY RANDOM()"):
            yield json.loads(value) | {"state_code": state_code, "court_code": court_code}


    def stats(self) -> dict[str, int]:
        """
        Returns a dict of tableName -> count
        """
        tables = ["case_types", "act_types", "courts", "cases"]
        stats = {}
        for table in tables:
            stats[table] = self.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        return stats
