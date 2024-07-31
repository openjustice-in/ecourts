import os
import requests
from captcha import Captcha
from tempfile import mkstemp
from urllib.parse import urlencode
from entities import Court
import csv
import parsers

class ECourt:
    # TODO: Get this dynamically at init
    CSRF_MAGIC_PARAMS = {
        "__csrf_magic": "sid:10e5a2d1738a8d1d68945ef1e6dcb8bfef62a46a,1721977473"
    }
    BASE_URL = "https://hcservices.ecourts.gov.in/ecourtindiaHC"
    def __init__(self, court: Court):
        self.session = requests.Session()
        self.court = court
        self.captcha = Captcha(self.session)
        self.session.get(self.url("/"))

    def url(self, path):
        return self.BASE_URL + path

    def apimethod(path, court=False, csrf=True, parser=None):
        def decorator(func):
            def inner(self, **kwargs):
                extra_params = func(self, **kwargs) or {}
                params = {"action_code": func.__name__} | kwargs | extra_params
                if court:
                    params |= self.court.queryParams()
                if csrf:
                    params |= self.CSRF_MAGIC_PARAMS

                response = self.session.post(self.url(path), data=params)
                response.raise_for_status()
                if parser:
                    return parser(response.text)
                else:
                    return response.text

            return inner

        return decorator        

    @apimethod(path="/cases/s_casetype_qry.php")
    def showRecords(self, fromDate, toDate):
        return {
            "from_date": date,
            "to_date": date,
            "captcha": self.captcha.solve(session),
        }

    @apimethod(path="/cases/s_casetype_qry.php", csrf=False, court=True, parser=parsers.parse_options)
    def fillCaseType(self):
        pass


if __name__ == "__main__":
    session = requests.Session()
    for court in filter(
        lambda x: x["state_cd"] == "12", csv.DictReader(open("courts.csv"))
    ):
        f = get_orders(session, "02-05-2024", court)
        for x in f:
            print(x)
