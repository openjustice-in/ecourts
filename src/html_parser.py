from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import sys
import re

@dataclass
class Party:
    name: str

@dataclass
class Case:
    case_type: str
    filing_number: str
    filing_date: Optional[datetime]
    registration_number: str
    registration_date: Optional[datetime]
    cnr_number: str
    first_hearing_date: Optional[datetime]
    decision_date: Optional[datetime]
    case_status: str
    nature_of_disposal: str
    coram: Optional[str]
    bench: Optional[str]
    state: Optional[str]
    district: Optional[str]
    judicial: Optional[str]
    not_before_me: Optional[str] = ""
    petitioners: List[Party]
    respondents: List[Party]
    subordinate_court_info: Optional[Dict] = {}
    history: List[dict] = []
    category_details: Dict = {}
    objections: List[dict] = []

@dataclass
class HistoryEntry:
  cause_list_type: str
  judge: str
  business_on_date: Optional[datetime]
  hearing_date: Optional[datetime]
  purpose_of_hearing: str

@dataclass
class Objection:
  sr_no: str
  scrutiny_date: Optional[datetime]
  objection: str
  compliance_date: Optional[datetime]
  receipt_date: Optional[datetime]

def parse_date(date_str: Optional[str]) -> Optional[datetime]:
  if not date_str:
    return None
  date_formats = ["%d-%m-%y", "%dth %B %Y"]
  for fmt in date_formats:
    try:
      return datetime.strptime(date_str, fmt)
    except ValueError:
      pass
  return None

def extract_text(element):
  return element.text.strip() if element else None

def extract_case_details(soup: BeautifulSoup) -> Dict:
  case_details_div = soup.find('div', class_='case_details_table')
  case_details = {}
  if case_details_div:
    for label_element in case_details_div.find_all('label'):
      key = label_element.text.strip()
      value = label_element.next_sibling.strip()
      case_details[key] = value
  return case_details

def extract_case_status(soup: BeautifulSoup) -> Dict:
  case_status_div = soup.find('div', text=re.compile('Case Status'))
  case_status = {}
  if case_status_div:
    for label_element in case_status_div.find_all('label'):
      key = label_element.strong.text.strip()
      value = label_element.strong.next_sibling.strip()
      case_status[key] = value
  return case_status

def extract_parties(soup: BeautifulSoup) -> Dict[str, List[str]]:
  parties = {'petitioners': [], 'respondents': []}
  for div in soup.find_all('div', class_=lambda x: x in ['Petitioner_Advocate_table', 'Respondent_Advocate_table']):
    party_type = 'petitioners' if 'Petitioner' in div['class'] else 'respondents'
    parties[party_type].append(div.text.strip())
  return parties

def extract_history(soup: BeautifulSoup) -> List[HistoryEntry]:
  history_table = soup.find('table', id='historyheading').find_next('table')
  history = []
  if history_table:
    for row in history_table.find_all('tr')[1:]:
      cells = row.find_all('td')
      # Handle cases where there are less than 5 cells
      if len(cells) < 5:
          continue  # Skip rows with missing data
      history.append(HistoryEntry(
        cause_list_type=cells[0].text.strip(),
        judge=cells[1].text.strip(),
        business_on_date=parse_date(cells[2].text.strip() if len(cells) > 2 else None),
        hearing_date=parse_date(cells[3].text.strip() if len(cells) > 3 else None),
        purpose_of_hearing=cells[4].text.strip() if len(cells) > 4 else None
      ))
  return history


def extract_category_details(soup: BeautifulSoup) -> Dict:
  category_heading = soup.find('b', text=re.compile('Category'))
  category_details = {}
  if category_heading:
    category_table = category_heading.find_next_sibling('table')
    if category_table:
      for row in category_table.find_all('tr'):
        cells = row.find_all('td')
        category_details[cells[0].text.strip()] = cells[1].text.strip()
  return category_details

def extract_objection(soup: BeautifulSoup) -> List[Objection]:
  objection_heading = soup.find('b', text=re.compile('OBJECTION'))
  objections = []
  if objection_heading:
    objection_table = objection_heading.find_next_sibling('table')
    if objection_table:
      for row in objection_table.find_all('tr')[1:]:
        cells = row.find_all('td')
        objections.append(Objection(
          sr_no=cells[0].text.strip(),
          scrutiny_date=parse_date(cells[1].text.strip()),
          objection=cells[2].text.strip(),
          compliance_date=parse_date(cells[3].text.strip()),
          receipt_date=parse_date(cells[4].text.strip())
        ))
  return objections

def parse_case(html_content: str) -> Case:
  soup = BeautifulSoup(html_content, 'html.parser')

  case_details = extract_case_details(soup)
  case_status = extract_case_status(soup)
  parties = extract_parties(soup)
  history = extract_history(soup)
  category_details = extract_category_details(soup)
  objections = extract_objection(soup)

  case = Case(
      case_type=case_details.get('Case Type'),
      filing_number=case_details.get('Filing Number'),
      registration_number=case_details.get('Registration Number'),
      registration_date=parse_date(case_details.get('Registration Date')),
      cnr_number=case_details.get('CNR Number'),
      first_hearing_date=parse_date(get_value_after_colon(case_status, 'First Hearing Date')),
      decision_date=parse_date(get_value_after_colon(case_status, 'Decision Date')),
      case_status=case_status.get('Case Status'),
      nature_of_disposal=case_status.get('Nature of Disposal'),
      coram=get_value_after_colon(case_status, 'Coram'),
      bench=get_value_after_colon(case_status, 'Bench'),
      state=get_value_after_colon(case_status, 'State'),
      district=get_value_after_colon(case_status, 'District'),
      judicial=get_value_after_colon(case_status, 'Judicial'),
      not_before_me=get_value_after_colon(case_status, 'Not Before Me'),
      petitioners=[Party(name=p) for p in parties['petitioners']],
      respondents=[Party(name=p) for p in parties['respondents']],
      history=history,
      category_details=category_details,
      objections=objections
  )

  return case

def get_value_after_colon(data_dict: Dict, key: str) -> Optional[str]:
  value = data_dict.get(key, '')
  return value.split(':')[1].strip() if ':' in value else None

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: python script.py <html_file>")
    exit(1)

  with open(sys.argv[1], 'r') as f:
    html_content = f.read()

  case = parse_case(html_content)
  print(case)
