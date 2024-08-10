import os
import requests
from captcha import Captcha, CaptchaError
from collections.abc import Iterator
from tempfile import mkstemp
import time
from urllib.parse import urlencode
from entities import Court, CaseType,Case, Hearing, Order, ActType
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

    def url(self, path, queryParams={}):
        if len(queryParams) > 0:
            return self.BASE_URL + path + "?" + urlencode(queryParams)
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

                retries = 15

                while retries > 0:
                    try:
                        extra_params = func(self, *args, **kwargs) or {}
                        if len(extra_params) == 0:
                            params |= kwargs
                        else:
                            params |= extra_params
                        if 'captcha' in params and params['captcha'] == None:
                            breakpoint()
                        response = self.session.post(self.url(path), data=params, allow_redirects=False, timeout=(5, 10))

                        # , headers={
                        #     "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
                        # })
                        self.validate_response(response)
                        if response.status_code == 302 and response.headers['location'].startswith("errormsg"):
                            raise ValueError("Error: " + response.headers['location'])
                        response.raise_for_status()
                        retries = 0
                    except (CaptchaError,ValueError, requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                        time.sleep(1)
                        retries -= 1
                        if retries == 0:
                            raise Exception("Attemped 10 Retries, still failed")
                    except (requests.exceptions.HTTPError) as e:
                        time.sleep(5)
                        retries -= 1
                        if retries == 0:
                            raise Exception("Attemped 10 Retries, still failed")
                
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
        from parsers.hearing_details import parse_hearing_details
        hearing.details = parse_hearing_details(self._get_hearing_details(**params))

    def downloadOrder(self, order: Order, court_case: Case, filename: str):
        # display_pdf.php?filename, caseno=AB/3142/2018 | cCode=1 | appFlag= | cino=GAHC010225502018 |state_code=6
        assert order.filename != None
        assert court_case.case_type != None
        assert court_case.registration_number != None
        assert court_case.cnr_number != None
        queryParams = {
            "filename": order.filename,
            "caseno": f"{court_case.case_type}/{court_case.registration_number}",
            "cCode": self.court.court_code or "1",
            "state_code": self.court.state_code,
            "cino": court_case.cnr_number,
        }
        url = self.url("/cases/display_pdf.php", queryParams)
        r = self.session.get(url)
        with open(filename, "wb") as f:
            f.write(r.content)

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
        url = self.url(f"/cases/s_casetype.php?state_cd={self.court.state_code}&dist_cd=1&court_code={self.court.court_code or "1"}")
        # Setup initial cookies
        self.session.get(url)
        result = self._search_cases_by_case_type(case_type, status, year)
        return parse_cases(result)
    
    # Search for cases by Act Type
    @apimethod(
        path="/cases/s_actwise_qry.php", action="showRecords", court=True, csrf=True
    )
    def _search_cases_by_act_type(self, act_type: str, status: str, **kwargs):
        """
        Search a specific ecourt for cases by act type under
        which they were registered. Requires a act type
        """
        assert status in ["Pending", "Disposed"]

        return {
            "captcha": self.captcha.solve(),
            "f": status,
            "actcode": act_type
        }

    def ActType(self, act_type:str, status:str):
        result = self._search_cases_by_act_type(act_type, status)
        return parse_cases(result)

    @apimethod(path="/cases/o_civil_case_history.php", court=True, action=None, csrf=False)
    def getCaseHistory(self, case: Case, **kwargs):
        return case.expandParams()

    # TODO: Store the case_type if available inside the case itself
    @apimethod(path="/cases/case_no_qry.php", action="showRecords", court=True)
    def searchSingleCase(self, registration_number: str, case_type: str):
        return {
            "captcha": self.captcha.solve(),
            "case_type": case_type,
            "case_no": registration_number.split("/")[0],
            "rgyear": registration_number.split("/")[1],
            "caseNoType": "new",
            "displayOldCaseNo": "NO"
        }


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

    def getCaseTypes(self) -> Iterator[CaseType]:
        for option in parse_options(self._get_case_type())[1:]:
            yield CaseType(code=int(option[0]), description=option[1], court=self.court)

    @apimethod(
        path="/cases/s_casetype_qry.php", csrf=True, court=True, action="fillCaseType"
    )
    def _get_case_type(self, *args, **kwargs):
        pass
    
    @apimethod(
        path="/cases/s_actwise_qry.php", csrf=False, court=True, action="fillActType"
    )  
    def _get_act_type(self, query: str, **kwargs):
        return {
            "search_act": query
        }

    def getActTypes(self, query="") -> Iterator[ActType]:
        for option in parse_options(self._get_act_type(query))[1:]:
            yield ActType(code=int(option[0]), description=option[1], court=self.court)

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
