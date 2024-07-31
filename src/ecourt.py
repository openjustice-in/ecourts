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
        "__csrf_magic": "sid:8de4600a644d2c934a43b04947504972f27b91d1,1722425086"
    }
    BASE_URL = "https://hcservices.ecourts.gov.in/ecourtindiaHC"
    def __init__(self, court: Court):
        self.session = requests.Session()
        self.court = court
        self.captcha = Captcha(self.session)
        self.session.get(self.url("/"))

    def enableDebug(self):
        self.captcha.debug = True

    def url(self, path):
        return self.BASE_URL + path

    def apimethod(path, court=False, csrf=True):
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
                return response.text

            return inner

        return decorator        

    @apimethod(path="/cases/s_orderdate_qry.php", court=True, csrf=True)
    def showRecords(self, **kwargs):
        return {
            "captcha": self.captcha.solve(),
        }

    def getOrdersOnDate(self, date: datetime.date):
        d = date.strftime("%d-%m-%Y")
        return parse_orders(self.showRecords(from_date=d, to_date=d))

    def getCaseTypes(self):
        for option in parse_options(self.fillCaseType())[1:]:
            yield CaseType(
                code=int(option[0]),
                description=option[1],
                court=self.court
            )


    @apimethod(path="/cases/s_casetype_qry.php", csrf=False, court=True)
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
