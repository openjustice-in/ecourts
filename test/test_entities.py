import pytest
import glob
import datetime
from entities import Business, Court, Order
import os
import wat


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


def test_order():
    d = datetime.date(2024, 6, 5)
    c = Court(
        state_code="12", district_code="1", court_code=None, state_name=None, name=None
    )
    order = Order(
        filename="bzPoyUlszYLCUcCpirIpqD4zP7uYkWTX8C00g6kf5Iussic1N%2FNtcHJ6pTca1m7D",
        case_number="\ufeffLPA/16/2024",
        cino="JKHC020004102024",
        court=c,
        judge="",
        date=d,
        appFlag="",
        judgement=False,
    )
    assert order.case_number == "LPA/16/2024"
    assert order.queryParams() == {
        "filename": "bzPoyUlszYLCUcCpirIpqD4zP7uYkWTX8C00g6kf5Iussic1N%2FNtcHJ6pTca1m7D",
        "caseno": "LPA/16/2024",
        "cCode": None,
        "appFlag": "",
        "cino": "JKHC020004102024",
        "state_code": "12",
    }
