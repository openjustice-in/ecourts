import pytest
import os
from storage import Storage
from entities import Court,CaseType
import sqlite3
import csv
import json

def test_storage_init():
    storage = Storage("/tmp/ecourts.db")
    assert os.path.exists("/tmp/ecourts.db")

    tables = storage.conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    assert len(tables) == 2
    assert "case_types" in tables[0]
    assert "courts" in tables[1]

    os.unlink("/tmp/ecourts.db")

def test_courts_add():
    storage = Storage("/tmp/ecourts.db")
    courts = list(Court.enumerate())
    storage.addCourts(courts)
    records = storage.conn.execute("SELECT * FROM courts").fetchall()
    assert len(records) ==  39
    for record in records:
        court = Court(**json.loads(record["value"]))
        assert court in courts
    os.unlink("/tmp/ecourts.db")

def test_case_types():
    storage = Storage("/tmp/ecourts.db")
    with open("case-types.csv") as f:
        reader = csv.reader(f)
        case_types = [CaseType(code=int(row[0]), description=row[1], court=Court(state_code=row[2], court_code=row[3] or None)) for row in reader][0:100]
        storage.addCaseTypes(case_types)
    for record in storage.getCaseTypes():
        assert record in case_types
    os.unlink("/tmp/ecourts.db")
