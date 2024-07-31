from dataclasses import dataclass
from collections import OrderedDict
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import urllib.parse
import sys
import re
from parsers.utils import parse_js_call, clean_html
from entities import Case, Party, HistoryEntry, Business, Order, Objection, Court


class CaseDetails:

    def extract_case_details(self, soup: BeautifulSoup) -> Dict:
        case_details = {}
        for label in soup.select("span.case_details_table label"):
            key = label.text.strip()
            value = ""
            if "Number" not in key and "Date" not in key and "Type" not in key:
                continue
            if label.next_sibling and label.next_sibling.name == "label":
                value = label.next_sibling.text.replace(":", "")
            elif ":" in label.parent.text:
                value = label.parent.text.split(":")[1]
            else:
                value = label.parent.next_sibling.text.split(":")[1]
            case_details[key] = value.strip().replace("\xa0", "")
        return case_details

    def extract_case_status(self, soup: BeautifulSoup) -> Dict:
        case_status_div = soup.find("h2", string=re.compile("Case Status"))
        case_status = {}

        for row in case_status_div.nextSibling.select("label"):
            if row.name == "label":
                [key, value] = row.find_all("strong")
                case_status[key.text.strip()] = value.text.split(":")[1].strip()
        return case_status

    def extract_parties(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        def extract_row(str):
            return str[3:]

        parties = {"petitioners": [], "respondents": []}
        for table in soup.find_all(
            "span",
            class_=lambda x: x
            in ["Petitioner_Advocate_table", "Respondent_Advocate_table"],
        ):
            party_type = (
                "petitioners" if "Petitioner" in table["class"][0] else "respondents"
            )
            parties[party_type].append(extract_row(table.text.strip()))
        return parties

    def extract_history(self, soup: BeautifulSoup) -> List[HistoryEntry]:
        history_table = soup.find("table", id="historyheading").find_next("table")
        history = []
        if history_table:
            for row in history_table.find_all("tr")[1:]:
                cells = row.find_all("td")
                # Handle cases where there are less than 5 cells
                if len(cells) < 5:
                    continue  # Skip rows with missing data
                type = cells[0].text.strip()
                if cells[2].select_one("a"):
                    # function viewBusiness(court_code,dist_code,n_dt,case_number,state_code,businessStatus,todays_date1,court_no,srno)
                    # TODO: perhaps use a Court instance?
                    signature = OrderedDict(
                        [
                            ("court_code", str),
                            ("dist_code", str),
                            ("nextdate1", str),
                            ("case_number1", str),
                            ("state_code", str),
                            ("disposal_flag", str),
                            ("businessDate", str),
                            ("court_no", str),
                            ("srno", str),
                        ]
                    )
                    res = parse_js_call(cells[2].select_one("a")["onclick"], signature)

                history.append(
                    HistoryEntry(
                        cause_list_type=type == type if type != "" else None,
                        judge=cells[1].text.strip(),
                        business_on_date=(
                            cells[2].text.strip() if len(cells) > 2 else None
                        ),
                        hearing_date=cells[3].text.strip() if len(cells) > 3 else None,
                        purpose_of_hearing=(
                            cells[4].text.strip() if len(cells) > 4 else None
                        ),
                        business=Business(**res) if res else None,
                    )
                )
        return history

    def extract_orders(self, soup: BeautifulSoup) -> List[Order]:
        orders = []
        for row in (
            soup.find("table", id="orderheading").find_next("table").find_all("tr")[1:]
        ):
            (_, caseno, judge, date, details) = row.find_all("td")
            url = details.select_one("a")["href"]

            query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            orders.append(
                Order(
                    case_number=query["caseno"][0].strip(),
                    judge=judge.text.strip(),
                    date=date.text.strip(),
                    filename=query["filename"][0].strip(),
                    court=Court(
                        query["state_code"][0].strip(), query["cCode"][0].strip()
                    ),
                    appFlag=query["appFlag"][0].strip() if "appFlag" in query else None,
                    cino=query["cino"][0].strip(),
                )
            )
        return orders

    def extract_category_details(self, soup: BeautifulSoup) -> Dict:
        category_details = {}
        for t in soup.find_all("table"):
            if "Category Details" in t.text:
                category_table = t.find_next("table")
                if category_table:
                    for row in category_table.find_all("tr"):
                        (key, value) = row.find_all("td")
                        category_details[key.text.strip()] = value.text.strip()
        return category_details

    def extract_objection(self, soup: BeautifulSoup) -> List[Objection]:
        objections = []
        for t in soup.find_all("table"):
            if "OBJECTION" in t.text:
                objection_table = t.find_next("table")
                if objection_table:
                    for row in objection_table.find_all("tr")[1:]:
                        (
                            _,
                            scrutiny_date,
                            objection_text,
                            compliance_date,
                            receipt_date,
                        ) = row.find_all("td")
                        objections.append(
                            Objection(
                                scrutiny_date=scrutiny_date.text.strip(),
                                objection=objection_text.text.strip(),
                                compliance_date=compliance_date.text.strip(),
                                receipt_date=receipt_date.text.strip(),
                            )
                        )
        return objections

    def __init__(self, html_content: str):
        soup = BeautifulSoup(html_content, "html.parser")

        case_details = self.extract_case_details(soup)
        case_status = self.extract_case_status(soup)
        parties = self.extract_parties(soup)
        history = self.extract_history(soup)
        category_details = self.extract_category_details(soup)
        objections = self.extract_objection(soup)
        orders = self.extract_orders(soup)

        self.case = Case(
            case_type=case_details.get("Case Type"),
            filing_number=case_details.get("Filing Number"),
            filing_date=case_details.get("Filing Date"),
            registration_number=case_details.get("Registration Number"),
            registration_date=case_details.get("Registration Date"),
            cnr_number=case_details.get("CNR Number"),
            first_hearing_date=case_status["First Hearing Date"],
            decision_date=case_status["Decision Date"],
            case_status=case_status.get("Case Status"),
            nature_of_disposal=case_status.get("Nature of Disposal"),
            coram=case_status["Coram"],
            bench=case_status["Bench"],
            state=case_status["State"],
            district=case_status["District"],
            judicial=case_status["Judicial"],
            not_before_me=case_status["Not Before Me"],
            petitioners=[Party(name=p) for p in parties["petitioners"]],
            respondents=[Party(name=p) for p in parties["respondents"]],
            history=history,
            category=category_details.get("Category"),
            sub_category=category_details.get("Sub Category"),
            objections=objections,
            orders=orders,
        )
        self.html = clean_html(soup)
