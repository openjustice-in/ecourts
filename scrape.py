import os
import requests
from captcha import decaptcha
from tempfile import mkstemp
from urllib.parse import urlencode
import csv

CSRF_MAGIC = "sid:10e5a2d1738a8d1d68945ef1e6dcb8bfef62a46a,1721977473"

def solve_captcha(session, retry=3):
    while retry > 0:
        captcha = session.get("https://hcservices.ecourts.gov.in/ecourtindiaHC/securimage/securimage_show.php")
        _, captcha_path = mkstemp(dir="captcha", suffix=".png")
        with open(captcha_path, "wb+") as f:
            f.write(captcha.content)

        res = decaptcha(os.path.basename(captcha_path))
        if res:
            return res.strip()
        else:
            retry -= 1
        # os.remove(captcha_path)

def parse_orders(raw_data):
    """Processes raw data and returns a list of case dictionaries.

    Args:
    raw_data: The input data string.

    Returns:
    A list of dictionaries, each representing a case.
    """

    data_parts = raw_data.split('^^')
    if "ERROR" in data_parts[0].upper() or "INVALID CAPTCHA" in data_parts[0].upper():
        raise ValueError("Got invalid result")
    for record_block in data_parts[0].split('##'):
        record_fields = record_block.split('~')
        if len(record_fields) < 10:
            continue

        if record_fields[7] == 'Y' or record_fields[7] == 'y' or record_fields[5] != '@#' or record_fields[6] != "":
            print(record_fields)
            raise NotImplementedError()

        case_data = {
            'number': record_fields[0],
            'date': record_fields[1],
            'fileid': record_fields[2],
            'judgement': 'JUDGEMENT' in record_fields[3],
            'court_code': record_fields[4],
            'cino': record_fields[8],
            'court_code': record_fields[9],
        }
        yield case_data


def get_orders(session, date, court):
    data = {
        "__csrf_magic" : CSRF_MAGIC,
        "action_code":"showRecords",
        "state_code":court['state_cd'],
        "dist_code":court['dist_cd'],
        "from_date":date,
        "to_date":date,
        "captcha":solve_captcha(session),
        "court_code":court['court_code']
    }
    response = session.post('https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate_qry.php',data=data)
    return parse_orders(response.text)

if __name__ == "__main__":
    session = requests.Session()
    for court in filter(lambda x: x['state_cd'] == '12', csv.DictReader(open('courts.csv'))):
        f = get_orders(session, "02-05-2024", court)
        for x in f:
            print(x)