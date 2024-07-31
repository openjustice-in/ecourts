import pytest
import glob
import datetime
from entities import Business, Court
import os


def test_courts_generator():
    courts = list(Court.enumerate())
    assert len(courts) == 39

    assert courts[0].state_code == "1"
    assert courts[0].district_code == "1"
    assert courts[0].court_code == None
    assert courts[0].queryParams() == {"state_code": "1", "dist_code": "1"}
    assert courts[5].queryParams() == {
        "state_code": "1",
        "dist_code": "1",
        "court_code": "6",
    }


def test_business():
    b = Business(
        court_code="1",
        dist_code="1",
        nextdate1="",
        case_number1="201700000582018",
        state_code="12",
        disposal_flag="Disposed",
        businessDate="24-12-2020",
        court_no="1712",
        srno="0",
    )
    assert b.businessDate == datetime.date(2020, 12, 24)
