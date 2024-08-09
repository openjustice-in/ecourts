import os
import requests
from captcha import Captcha
from tempfile import mkstemp
from urllib.parse import urlencode
from entities import Court, CaseType
import datetime
import csv
from parsers.orders import parse_orders
from parsers.options import parse_options


class ECourt:
    # TODO: Get this dynamically at init
    CSRF_MAGIC_PARAMS = {
        "__csrf_magic": "sid:c3dfc4837255ac20c67ef57089d64ecd2a636f92,1723203168"
    }
    BASE_URL = "https://hcservices.ecourts.gov.in/ecourtindiaHC"

    def __init__(self, court: Court):
        self.session = requests.Session()
        self.court = court
        self.captcha = Captcha(self.session)
        # We fetch the causelist for a far future date
        # to initialize our session
        self.get_cause_list(date=datetime.date(2034, 12, 31))

    def enableDebug(self):
        self.captcha.debug = True

    def url(self, path):
        return self.BASE_URL + path

    def apimethod(path, court=False, csrf=True, action=None):
        def decorator(func):
            def inner(self, **kwargs):
                extra_params = func(self, **kwargs) or {}
                action_params = {"action_code": action} if action else {}
                params = action_params | kwargs | extra_params
                if court:
                    params |= self.court.queryParams()
                if csrf:
                    params |= self.CSRF_MAGIC_PARAMS

                response = self.session.post(self.url(path), data=params)
                response.raise_for_status()
                return response.text

            return inner

        return decorator

    @apimethod(
        path="/cases/s_orderdate_qry.php", court=True, csrf=True, action="showRecords"
    )
    def _get_orders(self, **kwargs):
        return {
            "captcha": self.captcha.solve(),
        }

    # Search for cases by Case Type | 🚧WIP | Case Type, Year†, Pending/Disposed
    @apimethod(
        path="/cases/s_casetype_qry.php", action="ShowRecords", court=True, csrf=True
    )
    def _search_cases_by_case_type(self, case_type, status):
        assert status in ["Pending", "Disposed"]

        r = {"captcha": self.captcha.solve(), "f": status}
        if year:
            r["search_year"] = year
        return r

    @apimethod(path="/cases/o_civil_case_history.php", court=True, action=None)
    def getCaseHistory(self, cino: str, token: str, case_no: str):
        return {"cino": cino, "token": token, "case_no": case_no}

    def getOrdersOnDate(self, date: datetime.date):
        d = date.strftime("%d-%m-%Y")
        return parse_orders(self._get_orders(from_date=d, to_date=d))

    def getCaseTypes(self):
        for option in parse_options(self._get_case_type())[1:]:
            yield CaseType(code=int(option[0]), description=option[1], court=self.court)

    @apimethod(
        path="/cases/s_casetype_qry.php", csrf=True, court=True, action="fillCaseType"
    )
    def _get_case_type(self):
        pass

    @apimethod(
        path="/cases/highcourt_causelist_qry.php",
        court=True,
        action="pulishedCauselist",
    )
    def get_cause_list(self, date: datetime.date):
        dt_str = date.strftime("%d-%m-%Y")
        return {
            "causelist_dt": dt_str,
        }
