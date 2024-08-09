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
    case_types = [
        CaseType(code=332,description="ABA - Cr. Anticipatory Bail Appln.",court=Court(state_code="1")),
        CaseType(code=335,description="ALP - Appln for Leave to Appeal(PVT.)",court=Court(state_code="1")),
        CaseType(code=334,description="ALS - Appln For Leave to Appeal(STATE)",court=Court(state_code="1")),
        CaseType(code=3,description="AO - Appeal from Order",court=Court(state_code="1")),
        CaseType(code=310,description="APEAL - Cr. Appeal",court=Court(state_code="1")),
        CaseType(code=330,description="APL - Criminal Appln. U/s 482",court=Court(state_code="1")),
        CaseType(code=321,description="APPA - Cr. Application in Appeal",court=Court(state_code="1")),
        CaseType(code=327,description="APPCO - Application in Cr. Conf.",court=Court(state_code="1")),
        CaseType(code=326,description="APPCP - Application in Cr. Cont. Petn.",court=Court(state_code="1")),
        CaseType(code=324,description="APPCR - Application In Cr. Reference",court=Court(state_code="1")),
    ]
    storage.addCaseTypes(case_types)
    for record in storage.getCaseTypes():
        assert record in case_types
    os.unlink("/tmp/ecourts.db")
