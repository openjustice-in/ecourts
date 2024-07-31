import pytest
import glob
from courts import Courts
import datetime
from entities import Business
import os


def test_courts_generator():
    courts = list(Courts())
    assert len(courts) == 39

    assert courts[0].state_cd == "1"
    assert courts[0].dist_cd == "1"
    assert courts[0].court_code == None


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
