from bs4 import BeautifulSoup
from entities.hearing import Hearing

def parse_hearing_details(html: str) -> dict[str:str]:
    """Processes raw data and returns details of a case hearing

    Args:
    html: HTML from s_show_business.php

    Returns:
    A dict of key->value
    """

    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 3:
            key = cells[0].text.strip()
            value = cells[2].text.strip()
            if len(value) > 3:
                data[key] = value

    return data
