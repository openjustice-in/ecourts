import pytest
import glob
from entities import Case, Party, Hearing, Order, Objection, Court
from parsers import parse_hearing_details
from parsers.cases import parse_cases
from parsers.case_details import CaseDetails
import datetime
import yaml
import os
import wat


@pytest.fixture(params=glob.glob("test/fixtures/case_details/*.html"))
def case_details(request):
    cnr = os.path.splitext(request.param)[0]
    expected = None
    if os.path.exists(f"{cnr}.yml"):
        expected = yaml.unsafe_load(open(f"{cnr}.yml", "r"))
    yield [open(request.param, "r").read(), expected]


@pytest.fixture(params=glob.glob("test/fixtures/cases/*.txt"))
def case_row(request):
    yield open(request.param, "r").read()


@pytest.fixture(params=glob.glob("test/fixtures/hearings/*.html"))
def hearing(request):
    case_no = os.path.splitext(request.param)[0]
    expected = None
    if os.path.exists(f"{case_no}.yml"):
        expected = yaml.unsafe_load(open(f"{case_no}.yml", "r"))
    yield [open(request.param, "r").read(), case_no, expected]


def test_case_details_parser(case_details):
    html = case_details[0]
    expected = case_details[1]
    case_details = CaseDetails(html)

    if not expected:
        with open(
            f"test/fixtures/case_details/{case_details.case.cnr_number}.yml", "w"
        ) as f:
            yaml.dump(case_details.case, f)

    assert case_details.case == expected
    # We validate that our HTML is minimal and complete
    case_details2 = CaseDetails(case_details.html)

    # for some reason, beautifulsoup changes newlines slightly the second time around
    assert case_details2.html.replace("\n", "") == case_details.html.replace("\n", "")

    assert (
        case_details2.case == case_details.case
    )  # and the parser output should be equivalent
    assert (
        case_details2.case == case_details.case
    )  # and the parser output should be equivalent

    # Validate that we have minified the HTML by a factor of 2
    assert len(html) / len(case_details.html) > 2


def test_cases_parser(case_row):
    for case_obj in parse_cases(case_row):
        # if file exists
        fn = f"test/fixtures/cases/{case_obj.cnr_number}.yml"
        if os.path.exists(fn):
            with open(fn, "r") as f:
                expected = yaml.unsafe_load(f)
                assert case_obj == expected
        else:
            with open(fn, "w") as f:
                yaml.dump(case_obj, f)


def test_hearing_details_parser(hearing):
    html = hearing[0]
    case_no_file = hearing[1]
    expected = hearing[2]
    data = parse_hearing_details(html)
    if not expected:
        with open(f"{case_no_file}.yml", "w") as f:
            yaml.dump(data, f)
    else:
        assert data == expected
