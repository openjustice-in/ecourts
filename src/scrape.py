import os
import requests
from captcha import decaptcha
from tempfile import mkstemp
from urllib.parse import urlencode
import csv
import parser

class ECourt:
    # TODO: Get this dynamically at init
    CSRF_MAGIC = "sid:10e5a2d1738a8d1d68945ef1e6dcb8bfef62a46a,1721977473"
    def __init__(self, court):
        self.session = requests.Session()
        self.court = court

    def url(self, path):
        return f"https://hcservices.ecourts.gov.in/ecourtindiaHC{path}"

    def apimethod(path, court=False, csrf=True):
        def decorator(func):
            def inner(self, **kwargs):
                extra_params = func(self, **kwargs) or {}
                params = {"action_code": func.__name__} | kwargs | extra_params
                return api(self, path, params, court, csrf)

            return inner

        return decorator

    def api(self, path, params, court, csrf=True):
        if csrf:
            params["__csrf_magic"] = self.CSRF_MAGIC
        if court:
            params = params | court_params(court)
        response = self.session.post(self.url(path), data=params)
        response.raise_for_status()
        return response.text

    def court_params(self, court):
        return {
            "state_code": court.state_cd,
            "dist_code": court.dist_cd,
            "court_code": court.court_code,
        }

    @apimethod(path="/cases/s_casetype_qry.php")
    def showRecords(self, fromDate, toDate):
        return {
            "from_date": date,
            "to_date": date,
            "captcha": solve_captcha(session),
        }

    @api(path="/cases/s_casetype_qry.php", csrf=False, parser=parser.Options)
    def fillCaseType(self, **kwargs):
        pass


if __name__ == "__main__":
    session = requests.Session()
    for court in filter(
        lambda x: x["state_cd"] == "12", csv.DictReader(open("courts.csv"))
    ):
        f = get_orders(session, "02-05-2024", court)
        for x in f:
            print(x)
