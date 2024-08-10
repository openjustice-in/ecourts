import os
import requests
from captcha import Captcha, CaptchaError
from tempfile import mkstemp
from urllib.parse import urlencode
from entities import Court, CaseType,Case, Hearing
from entities.hearing import UnexpandableHearing
import datetime
import csv
from parsers.orders import parse_orders
from parsers.options import parse_options
from parsers.cases import parse_cases


class ECourt:
    # TODO: Get this dynamically at init
    CSRF_MAGIC_PARAMS = {
        "__csrf_magic": "sid:e2b2b2ae5e125f3174066a01e182acd472a256ea,1723269931"
    }
    BASE_URL = "https://hcservices.ecourts.gov.in/ecourtindiaHC"

    def __init__(self, court: Court):
        self.session = requests.Session()
        self.court = court
        self.captcha = Captcha(self.session)

    def enableDebug(self):
        self.captcha.debug = True

    def url(self, path):
        return self.BASE_URL + path

    def validate_response(self, r):
        t = r.text.upper()[0:30]
        if "ERROR" in t:
            raise ValueError("Got invalid result")
        if "INVALID CAPTCHA" in t:
            raise CaptchaError()

    def apimethod(path, court=False, csrf=True, action=None):
        def decorator(func):
            def inner(self, *args, **kwargs):
                params = {"action_code": action} if action else {}
                if court:
                    params |= self.court.queryParams()
                if csrf:
                    params |= self.CSRF_MAGIC_PARAMS

                retries = 5

                while retries > 0:
                    extra_params = func(self, *args, **kwargs) or {}
                    if len(extra_params) == 0:
                        params |= kwargs
                    else:
                        params |= extra_params
                    try:
                        response = self.session.post(self.url(path), data=params, allow_redirects=False)
                        self.validate_response(response)
                        if response.status_code == 302 and response.headers['location'].startswith("errormsg"):
                            raise ValueError("Error: " + response.headers['location'])
                        retries = 0
                    except (CaptchaError,ValueError) as e:
                        retries -= 1
                        if retries == 0:
                            raise Exception("Attemped 5 Retries, still failed")
                
                response.raise_for_status()
                response.encoding = "utf-8-sig"
                return response.text

            return inner

        return decorator

    @apimethod(
        path="/cases/s_orderdate_qry.php", court=True, csrf=True, action="showRecords"
    )
    def _get_orders(self, *args, **kwargs):
        return {
            "captcha": self.captcha.solve(),
        }

    @apimethod(
        path="/cases/s_show_business.php", court=True, csrf=False, action=None
    )
    def _get_hearing_details(self, *args, **kwargs):
        pass

    def expandHearing(self, hearing: Hearing, case: Case):
        """
        Expand a hearing object with more details from the daily business list
        """
        if case.case_number == None:
            raise ValueError("Require a case.case_number to expand hearing details")
        if hearing.court_no == None or hearing.srno == None or hearing.date == None:
            raise UnexpandableHearing()
        params = {
            "case_number1": case.case_number,
        } | hearing.expandParams()
        hearing.details = self._get_hearing_details(**params)

    # Search for cases by Case Type | 🚧WIP | Case Type, Year†, Pending/Disposed
    @apimethod(
        path="/cases/s_casetype_qry.php", action="showRecords", court=True, csrf=True
    )
    def _search_cases_by_case_type(self, case_type, status, search_year, **kwargs):
        assert status in ["Pending", "Disposed"]

        r = {
            "captcha": self.captcha.solve(),
            "f": status,
            "case_type": case_type
        }
        if search_year:
            r["search_year"] = search_year
        return r

    def CaseType(self, case_type:str, status:str, year: int = None):
        result = self._search_cases_by_case_type(case_type, status, year)
        return parse_cases(result)

    @apimethod(path="/cases/o_civil_case_history.php", court=True, action=None, csrf=False)
    def getCaseHistory(self, case: Case, **kwargs):
        return case.expandParams()

    def expand_case(self, case: Case):
        from parsers.case_details import CaseDetails
        html = self.getCaseHistory(case)
        newcase = CaseDetails(html).case
        if case.case_number:
            newcase.case_number = case.case_number
        return newcase

    def getOrdersOnDate(self, date: datetime.date):
        d = date.strftime("%d-%m-%Y")
        return parse_orders(self._get_orders(from_date=d, to_date=d))

    def getCaseTypes(self):
        for option in parse_options(self._get_case_type())[1:]:
            yield CaseType(code=int(option[0]), description=option[1], court=self.court)

    @apimethod(
        path="/cases/s_casetype_qry.php", csrf=True, court=True, action="fillCaseType"
    )
    def _get_case_type(self, *args, **kwargs):
        pass

    @apimethod(
        path="/cases/highcourt_causelist_qry.php",
        court=True,
        action="pulishedCauselist",
        csrf=False
    )
    def get_cause_list(self, date: datetime.date, **kwargs):
        dt_str = date.strftime("%d-%m-%Y")
        return {
            "causelist_dt": dt_str,
        }
