import pytest
from entities import Court, CaseType, Order, Case,Party
from entities.hearing import UnexpandableHearing
from ecourt import ECourt
import os
import datetime
import yaml


@pytest.mark.vcr()
def test_api_calls():
    ecourt = ECourt(Court(state_code="12", district_code="1"))
    options = list(ecourt.getCaseTypes())
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
    d = datetime.date(2024, 6, 5)
    c = Court(
        state_code="12", district_code="1", court_code=None, state_name=None, name=None
    )

    orders = list(ecourt.getOrdersOnDate(d))
    kw = {"judge": "", "date": d}
    assert orders[0:10] == [
        Order(
            filename="bzPoyUlszYLCUcCpirIpqD4zP7uYkWTX8C00g6kf5Iussic1N%2FNtcHJ6pTca1m7D",
            judgement=False,
            **kw,
        ),
        Order(
            filename="bzPoyUlszYLCUcCpirIpqK29mwVkw7QN%2B4LH%2FIs47MFZX1V6etNVnz%2BHz9lzGeUS",
            **kw,
            judgement=False,
        ),
        Order(
            filename="zDLovBVSUw02H8XukOjXfK%2FTsM5L1K0GA6SQAwByRzlC7wZ8dUxDpcjLcQ3zYzUE",
            **kw,
            judgement=False,
        ),
        Order(
            filename="bzPoyUlszYLCUcCpirIpqAUW%2FU5fQp5afvkYRpXJG3dKmom21n7DoOAbZ%2FOx1HPp",
            judgement=False,
            **kw,
        ),
        Order(
            filename="bzPoyUlszYLCUcCpirIpqDP6tRn7wRZuqetdseJcNgeEhuqNjXwfRbz5sDskf4sJ",
            judgement=True,
            **kw,
        ),
        Order(
            filename="bzPoyUlszYLCUcCpirIpqEnpY7p7aTz2fWQ4SSZfWxHkGo3jYtQHpc3Y9V5n0QdZ",
            judgement=True,
            **kw,
        ),
        Order(
            filename="bzPoyUlszYLCUcCpirIpqJYwz8NC3QX5gdpqdOWJBmuTG4yI0RybYiNLOcEusFak",
            judgement=False,
            **kw,
        ),
        Order(
            filename="bzPoyUlszYLCUcCpirIpqDtYFcOs7W9tDsMyW6hqcdbYIPQMvqrvd18sKcJkpwAa",
            judgement=False,
            **kw,
        ),
        Order(
            filename="bzPoyUlszYLCUcCpirIpqDIZYdIfqv7sL9bnU9QB5rLQFTBQfQNepZKCq0YW90sf",
            judgement=False,
            **kw,
        ),
        Order(
            filename="bzPoyUlszYLCUcCpirIpqIVkBt3UHmCGOsE%2B%2FU8K7XUob2sFWNoGPP%2BbpLNNCOef",
            judgement=False,
            **kw,
        ),
    ]

    ecourt.court.state_code = "16"
    ecourt.court.court_code = None
    assert list(ecourt.getCaseTypes())[0:10] == [
        CaseType(
            code=1,
            description="AA - ARBRITATION APPL.",
            court=ecourt.court,
        ),
        CaseType(
            code=2,
            description="ABWA - APPL.UND.BENGAL WAKFS ACT",
            court=ecourt.court,
        ),
        CaseType(
            code=3,
            description="AC - AWARD CASES",
            court=ecourt.court,
        ),
        CaseType(
            code=4,
            description="ACA - APPL.UNDER CHARTERED ACCOUNTANTS ACT, 1949",
            court=ecourt.court,
        ),
        CaseType(
            code=5,
            description="ACO - PET. IN COMP. APPL.",
            court=ecourt.court,
        ),
        CaseType(
            code=6,
            description="ACR - APPL.UND.CHARITABLE AND RELIGIOUS TRUST ACT",
            court=ecourt.court,
        ),
        CaseType(
            code=7,
            description="ACRP - APPL.UND.SEC.151 OF THE CR.P.C.",
            court=ecourt.court,
        ),
        CaseType(
            code=8,
            description="ACWA - APPL.UND.SEC 21 COST AND WORKS ACCOUNTACTS ACT, 1959",
            court=ecourt.court,
        ),
        CaseType(
            code=134,
            description="AD-COM - APPEAL FROM DECREES (COMMERCIAL)",
            court=ecourt.court,
        ),
        CaseType(
            code=9,
            description="AED - APPL. U/S. 64 OF ESTATE DUTY ACT, 1953",
            court=ecourt.court,
        ),
    ]


@pytest.mark.vcr()
def test_case_history():
    ecourt = ECourt(Court(state_code="3"))
    ecourt.getCaseHistory(
        case=Case(
            case_type="CRL.P",
            registration_number="5658/2024",
            cnr_number="KAHC010337682024",
            token="14b7927a52c474a5c85379fe180635c8957638b3440506b816c755af53b91990",
            case_number="211200056582024",
        )
    )

@pytest.mark.vcr()
def test_get_act_type():
    court = Court(state_code="3")
    ecourt = ECourt(court)
    v = []
    for act in  ecourt.getActTypes():
        assert act.court == court
        v.append((act.code, act.description))

    assert v[0:14] == [
        (172, 'Admirality (Jurisdiction and Settlement of Maritime Claims) Act'),
        (156, 'Air (Prevention and Control of Pollution) Rules (Maharashtra)'),
        (106, 'ARBITRATION AND CONCILIATION ACT'),
        (170, 'Central Excises Act'),
        (184, 'Central Goods and Service Tax Act'),
        (102, 'CODE OF CIVIL PROCEDURE'),
        (103, 'CODE OF CRIMINAL PROCEDURE'),
        (134, 'Commercial Courts, Commercial Division and Commercial Appellate Division of High Courts Act, 201'),
        (104, 'COMPANIES ACT'),
        (105, 'Companies (Court) Rules'),
        (101, 'Constitution of India'),
        (181, 'DISASTER MANAGEMENT ACT'),
        (135, 'Employee&'),
        (39, 's Compensation Act')
    ]




@pytest.mark.vcr()
def test_case_expander():
    ecourt = ECourt(Court(state_code="6"))
    cases = ecourt.CaseType("49", "Pending", "2018")
    fcase = next(cases)

    assert fcase.case_type == "AB"
    assert fcase.registration_number == "3142/2018"
    assert fcase.cnr_number == "GAHC010225502018"
    assert fcase.petitioners[0].name == "ANURAG TANKHA"
    assert fcase.respondents[0].name == "THE STATE OF ASSAM"
    assert fcase.case_number == "204900031422018"

    assert fcase.expandParams()['cino'] == "GAHC010225502018"
    assert fcase.expandParams()['case_no'] == "204900031422018"
    assert len(fcase.expandParams()['token']) == 64

    fcase2 = ecourt.expand_case(fcase)
    with open("test/fixtures/cases/GAHC010225502018.yml", 'w') as f:
        yaml.dump(fcase2, f)

    for hearing in fcase2.hearings:
        try:
            ecourt.expandHearing(hearing, fcase2)
            assert len(hearing.details) > 0
        except UnexpandableHearing as e:
            pass

    order = fcase2.orders[0]
    ecourt.downloadOrder(order, fcase2, "/tmp/GAHC010225502018-01.pdf")
    assert os.path.getsize("/tmp/GAHC010225502018-01.pdf") == 75073
