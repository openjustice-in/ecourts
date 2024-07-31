import pytest
from ecourt import ECourt
from entities import Court, CaseType, Order
import datetime

@pytest.mark.vcr()
def test_api_calls():
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
    d = datetime.date(2024,6,5)
    c = Court(state_code='12', district_code='1', court_code=None, state_name=None, name=None)

    orders = list(scraper.getOrdersOnDate(d))
    assert orders[0:10] == [
        Order(filename='bzPoyUlszYLCUcCpirIpqD4zP7uYkWTX8C00g6kf5Iussic1N%2FNtcHJ6pTca1m7D', case_number='LPA/16/2024', cino='JKHC020004102024', court=c, judge='', date=d, appFlag='', judgement=False),
        Order(filename='bzPoyUlszYLCUcCpirIpqK29mwVkw7QN%2B4LH%2FIs47MFZX1V6etNVnz%2BHz9lzGeUS', case_number='LPA/18/2024', cino='JKHC020005482024', court=c, judge='', date=d, appFlag='', judgement=False),
        Order(filename='zDLovBVSUw02H8XukOjXfK%2FTsM5L1K0GA6SQAwByRzlC7wZ8dUxDpcjLcQ3zYzUE', case_number='LPA/22/2023', cino='JKHC020059712022', court=c, judge='', date=d, appFlag='', judgement=False),
        Order(filename='bzPoyUlszYLCUcCpirIpqAUW%2FU5fQp5afvkYRpXJG3dKmom21n7DoOAbZ%2FOx1HPp', case_number='LPA/77/2024', cino='JKHC020018322024', court=c, judge='', date=d, appFlag='', judgement=False),
        Order(filename='bzPoyUlszYLCUcCpirIpqDP6tRn7wRZuqetdseJcNgeEhuqNjXwfRbz5sDskf4sJ', case_number='LPA/89/2024', cino='JKHC020021152024', court=c, judge='', date=d, appFlag='', judgement=True),
        Order(filename='bzPoyUlszYLCUcCpirIpqEnpY7p7aTz2fWQ4SSZfWxHkGo3jYtQHpc3Y9V5n0QdZ', case_number='LPA/94/2024', cino='JKHC020022452024', court=c, judge='', date=d, appFlag='', judgement=True),
        Order(filename='bzPoyUlszYLCUcCpirIpqJYwz8NC3QX5gdpqdOWJBmuTG4yI0RybYiNLOcEusFak', case_number='LPA/115/2024', cino='JKHC020027142024', court=c, judge='', date=d, appFlag='', judgement=False),
        Order(filename='bzPoyUlszYLCUcCpirIpqDtYFcOs7W9tDsMyW6hqcdbYIPQMvqrvd18sKcJkpwAa', case_number='LPA/116/2024', cino='JKHC020029722024', court=c, judge='', date=d, appFlag='', judgement=False),
        Order(filename='bzPoyUlszYLCUcCpirIpqDIZYdIfqv7sL9bnU9QB5rLQFTBQfQNepZKCq0YW90sf', case_number='LPA/117/2024', cino='JKHC020025652024', court=c, judge='', date=d, appFlag='', judgement=False),
        Order(filename='bzPoyUlszYLCUcCpirIpqIVkBt3UHmCGOsE%2B%2FU8K7XUob2sFWNoGPP%2BbpLNNCOef', case_number='LPA/118/2024', cino='JKHC020029242024', court=c, judge='', date=d, appFlag='', judgement=False)
    ]
    assert orders[0].case_number == 'LPA/16/2024'
