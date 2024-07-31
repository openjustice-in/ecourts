import pytest
from scrape import ECourt
from entities import Court

@pytest.mark.vcr()
def test_get_court_order_types():
    scraper = ECourt(Court(state_code="12", district_code="1"))
    options = scraper.fillCaseType()
    assert len(options) == 233
    assert options[-1] == ('328', 'WP(Crl) - WRIT PETITION CRIMINAL', False)

