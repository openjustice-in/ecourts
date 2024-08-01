import pytest
import glob
from parsers.case_details import CaseDetails
from entities import Case, Party, Business, HistoryEntry, Order, Objection, Court
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


# def test_date_parser():
#     from parsers.utils import parse_date
#     wat / parse_date("Next Date is not given")


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
