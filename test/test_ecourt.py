import pytest
from ecourt import ECourt
from entities import Court, CaseType
import datetime

@pytest.mark.vcr()
def get_api_calls():
    scraper = ECourt(Court(state_code="12", district_code="1"))
    options = list(scraper.getCaseTypes())
    assert len(options) == 233
    assert options[-1] == CaseType(
        code=328,
        description="WP(Crl) - WRIT PETITION CRIMINAL",
        court=Court(
            state_code="12",
            district_code="1",
            court_code=None,
            state_name=None,
            name=None,
        ),
    )
    scraper.getOrdersOnDate(datetime.date(2024,6,5))
