import click
from entities import Court
from ecourt import ECourt
import csv
from sys import stdout

@click.command()
@click.option("--state-code", help="State code of the Court")
@click.option("--court-code", help="Court code of the Court")
def get_case_types(state_code, court_code):
    if state_code == None and court_code == None:
        courts =  Court.enumerate()
    else:
        courts = [Court(state_code=state_code, court_code=court_code)]
    for court in  courts:
        scraper = ECourt(court)
        types =  scraper.getCaseTypes()
        writer = csv.writer(stdout)
        for case_type in types:
            writer.writerow([case_type.code, case_type.description, court.state_code, court.court_code])


