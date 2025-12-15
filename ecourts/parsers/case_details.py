from dataclasses import dataclass
from collections import OrderedDict
from datetime import datetime
from typing import Optional
from bs4 import BeautifulSoup
import urllib.parse
import sys
import re
from parsers.utils import parse_js_call, clean_html
from entities import Case, Party, Hearing, Order, Objection, Court, FIR


class CaseDetails:

    def extract_span_label_dict(self, soup: BeautifulSoup) -> dict[str, str]:
        """
        Extracts key-value pairs from case_details_table spans, 
        using primary next_sibling method and a text-splitting fallback.
        """
        # Define the known valid key checks (moved inside the function)
        KNOWN_VALID_KEY_CHECKS: List[str] = [
            "Number", "Key", "Station", "District", "Year", "State", "Type", "Date"
        ]
        
        details = {}
        
        # Find all labels in case_details_table spans
        for label in soup.select('.case_details_table label'):
            key = label.text.strip()
            
            # Validate key contains at least one known check string
            if not any(check in key for check in KNOWN_VALID_KEY_CHECKS):
                continue
            
            value = ""
            
            # Method 1: Check for next named sibling label
            next_named_sibling = None
            for sibling in label.next_siblings:
                if sibling.name:
                    next_named_sibling = sibling
                    break
            
            if next_named_sibling and next_named_sibling.name == "label":
                value = next_named_sibling.text.replace(":", "").strip()
            # Method 2: Split parent text by ":"
            elif ":" in label.parent.text:
                parts = label.parent.text.split(":", 1)
                if len(parts) > 1:
                    value = parts[1].strip()
            # Method 3: Check parent's next siblings
            else:
                for sibling in label.parent.next_siblings:
                    if hasattr(sibling, 'text') and ":" in sibling.text:
                        parts = sibling.text.split(":", 1)
                        if len(parts) > 1:
                            value = parts[1].strip()
                            break
            
            # Clean up value
            details[key] = value.replace("\xa0", "").strip()
        
        return details
    def extract_case_details(self, soup: BeautifulSoup) -> dict:
        return self.extract_span_label_dict(soup)

    def extract_fir_details(self, soup: BeautifulSoup) -> dict:
        d = soup.select_one("span.FIR_details_table")
        if d:
            s = d.text.replace("\xa0", "").strip()
            regex = r"(?P<k>.*):\s?(?P<v>(\w|\d| )+)\s?"
            matches = re.finditer(regex, s, re.MULTILINE)
            fir_details = {}
            for matchNum, match in enumerate(matches, start=1):
                fir_details[match.group("k")] = match.group("v").strip()
            return fir_details

    def extract_case_status(self, soup: BeautifulSoup) -> dict:
        case_status_div = soup.find("h2", string=re.compile("Case Status"))
        case_status = {}

        if case_status_div == None:
            breakpoint()

        next_sibling = None
        for next_sibling in case_status_div.next_siblings:
            if next_sibling.name:
                break

        for row in next_sibling.select("label"):
            if row.name == "label":
                [key, value] = row.find_all("strong")
                case_status[key.text.strip()] = value.text.split(":")[1].strip()
        return case_status

    def extract_parties(self, soup: BeautifulSoup, spanClass: str) -> list[Party]:
        table = soup.find("span", class_=spanClass)
        if not table:
            raise ValueError("NO TABLES")
            return []
        s = table.text.replace("\xa0", "").strip()
        regex = r"\d\)\s+(?P<party>[^\n]+)(?:(?:\s|\n)+Advocate\s*-\s*(?P<advocate>[^\n]+))?"
        matches = re.finditer(regex, s, re.MULTILINE)
        parties = []
        for matchNum, match in enumerate(matches, start=1):
            party = Party(name=match.group("party").strip())
            if match.group("advocate"):
                party.advocate = match.group("advocate").strip()
            parties.append(party)
        return parties

    def extract_hearing(self, soup: BeautifulSoup) -> list[Hearing]:
        f = soup.find("table", id="historyheading")
        if f:
            history_table = f.find_next("table")
        else:
            return []
        history = []
        if history_table:
            for row in history_table.find_all("tr")[1:]:
                cells = row.find_all("td")
                # Handle cases where there are less than 5 cells
                if len(cells) < 5:
                    continue  # Skip rows with missing data
                cause_list_type = cells[0].text.strip()
                if len(cause_list_type) < 4 :
                    cause_list_type = None
                if cause_list_type == "Order Number":
                    break
                if cells[2].select_one("a"):
                    # function viewBusiness(court_code,dist_code,n_dt,case_number,state_code,businessStatus,todays_date1,court_no,srno)

                    signature = OrderedDict(
                        [
                            ("court_code", str),
                            ("district_code", str),
                            ("next_date", str),
                            ("case_number", str),
                            ("state_code", str),
                            ("disposal_flag", str),
                            ("business_date", str),
                            ("court_no", str),
                            ("srno", str),
                        ]
                    )
                    res = parse_js_call(cells[2].select_one("a")["onclick"], signature)
                    # We don't need court details since they should be in the parent entity
                    # # breakpoint()
                    # court = Court(
                    #     state_code=res.pop("state_code"),
                    #     district_code=res.pop("district_code"),
                    #     court_code=res.pop("court_code", None),
                    # )

                history.append(
                    Hearing(
                        cause_list_type = cause_list_type,
                        judge=cells[1].text.strip(),
                        date=(
                            cells[2].text.strip() if len(cells) > 2 else None
                        ),
                        next_date=cells[3].text.strip() if len(cells) > 3 else None,
                        purpose=(
                            cells[4].text.strip() if len(cells) > 4 else None
                        ),
                        court_no=res.get("court_no"),
                        srno=res.get("srno"),
                    )
                )
        return history

    def extract_orders(self, soup: BeautifulSoup) -> list[Order]:
        orders = []
        ordertable = soup.find("table", class_="order_table")
        if ordertable == None:
            import pytest
            pytest.set_trace()
        for row in ordertable.find_all("tr")[1:]:
            try:
                (_, caseno, judge, date, details) = row.find_all("td")
            except ValueError:
                print(row.find_all("td"))
            

            link = details.select_one("a")
            url = None
            if link:
                url = link["href"]
            else:
                print(soup)
                breakpoint()

            query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            orders.append(
                Order(
                    judge=judge.text.strip(),
                    date=date.text.strip(),
                    filename=query["filename"][0].strip(),
                )
            )
        return orders

    def extract_category_details(self, soup: BeautifulSoup) -> dict:
        category_details = {}
        for t in soup.find_all("table"):
            if "Category Details" in t.text:
                category_table = t.find_next("table")
                if category_table:
                    for row in category_table.find_all("tr"):
                        (key, value) = row.find_all("td")
                        category_details[key.text.strip()] = value.text.strip()
        return category_details

    def extract_objection(self, soup: BeautifulSoup) -> list[Objection]:
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
        if "session expired" in html_content:
            raise ValueError("Session expired")

        soup = BeautifulSoup(html_content, "html5lib")

        for br in soup.find_all("br"):
            br.replace_with("\n")

        case_details = self.extract_case_details(soup)
        fir_details = self.extract_fir_details(soup)
        fir = None
        if fir_details:
            fir = FIR(
                state=fir_details.get("State"),
                district=fir_details.get("District"),
                police_station=fir_details.get("Police Station"),
                number=fir_details.get("FIR Number"),
                year=fir_details.get("Year"),
            )
        case_status = self.extract_case_status(soup)
        petitioners = self.extract_parties(soup, "Petitioner_Advocate_table")
        respondents = self.extract_parties(soup, "Respondent_Advocate_table")
        hearings = self.extract_hearing(soup)
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
            first_hearing_date=case_status.get("First Hearing Date", None),
            decision_date=case_status.get("Decision Date", None),
            case_status=case_status.get(
                "Case Status",
                case_status.get("Stage of Case", None),
            ),
            nature_of_disposal=case_status.get("Nature of Disposal", None),
            coram=case_status.get("Coram", None),
            bench=case_status.get("Bench", None),
            state=case_status.get("State", None),
            district=case_status.get("District", None),
            judicial=case_status.get("Judicial", None),
            not_before_me=case_status["Not Before Me"],
            petitioners=petitioners,
            respondents=respondents,
            hearings=hearings,
            category=category_details.get("Category"),
            sub_category=category_details.get("Sub Category"),
            objections=objections,
            orders=orders,
            fir=fir,
        )
        self.html = clean_html(soup)
