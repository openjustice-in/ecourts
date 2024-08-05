import click
from entities import Court
from ecourt import ECourt
import csv
from sys import stdout
from datetime import datetime

import click
from datetime import datetime
from functools import wraps

def validate_year(ctx, _, value):
    if value and len(value) != 4:
        raise click.BadParameter('Year must be in YYYY format')
    return value

def validate_date(ctx, _, value):
    if value:
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise click.BadParameter('Date must be in YYYY-MM-DD format')
    return value

def setup_state_code(ctx, _, value):
    ctx.obj['state_code'] = value

def setup_court_code(ctx, _, value):
    ctx.obj['court'] = Court(ctx.obj['state_code'], value)

def common_options(f):
    @click.option('--case-number', help='Case number')
    @click.option('--party-name', help='Party name')
    @click.option('--case-type', type=int, help='Case type')
    @click.option('--year', callback=validate_year, help='Year in YYYY format')
    @click.option("--state-code", callback=setup_state_code, help="State code of the Court", required=True)
    @click.option("--court-code", callback=setup_court_code, help="Court code of the Court")
    @click.pass_context
    @wraps(f)
    def wrapper(ctx, *args, **kwargs):
        ctx.ensure_object(dict)
        for option in ['case_number', 'party_name', 'case_type', 'year']:
            if option in kwargs:
                ctx.obj[option] = kwargs[option]

        if not 'court' in ctx.obj:
            raise click.BadParameter('A valid state-code, court-code is required')
        return f(*args, **kwargs)
    return wrapper

@click.group()
@click.pass_context
def ecourts(ctx):
    """eCourts application for retrieving case information."""
    ctx.ensure_object(dict)

@ecourts.command()
@common_options
@click.option('--fir-number', help='FIR number')
@click.option('--filing-number', help='Filing number')
@click.option('--status', type=click.Choice(['Pending', 'Disposed']), help='Case status')
@click.option('--police-station-id', help='Police station ID')
@click.pass_context
def get_cases(ctx, case_number, party_name, case_type, year, state_code, court_code,
              fir_number, filing_number, status, police_station_id):
    court:Court = ctx.obj['court']
    ecourt = ECourt(court)

    if case_number and case_type and year:
        ecourt.search_by_case_number(case_type, case_number, year)
    elif police_station_id:
        ecourt.search_by_fir_number(police_station_id, fir_number, year, status)
    elif party_name:
        ecourt.search_by_party_name(party_name, year, status)
    elif filing_number and year:
        ecourt.search_by_filing_number(filing_number, year)
    elif case_type:
        if status == "Both":
            raise click.BadParameter('Case Status can either be Pending or Disposed for searching by case-type')
        ecourt.search_by_case_type(case_type, year, status)
    else:
        click.echo("Invalid combination of arguments. Please provide a valid set of options.")

@ecourts.command()
@common_options
@click.option('--filing-number', help='Filing number')
@click.option('--from-date', callback=validate_date, help='From date in YYYY-MM-DD format')
@click.option('--to-date', callback=validate_date, help='To date in YYYY-MM-DD format')
@click.pass_context
def get_orders(ctx, case_number, party_name, case_type, year, state_code, court_code,
               filing_number, from_date, to_date):
    """Get order information based on various search criteria."""
    if case_number and case_type and year:
        orders_case_number(state_code, court_code, case_type, case_number, year)
    elif filing_number and year:
        orders_filling_number(state_code, court_code, filing_number, year)
    elif party_name and year:
        orders_party_name(state_code, court_code, party_name, year)
    elif from_date and to_date:
        orders_order_date(state_code, court_code, from_date, to_date)
    else:
        click.echo("Invalid combination of arguments. Please provide a valid set of options.")

@ecourts.command()
@click.option("--state-code", help="State code of the Court")
@click.option("--court-code", help="Court code of the Court")
@click.pass_context
def get_case_types(ctx, state_code, court_code):
    if state_code == None and court_code == None:
        courts = Court.enumerate()
    else:
        courts = [Court(state_code, court_code)]
    
    for court in courts:
        scraper = ECourt(court)
        types = scraper.getCaseTypes()
        writer = csv.writer(stdout)
        for case_type in types:
            writer.writerow(
                [
                    case_type.code,
                    case_type.description,
                    court.state_code,
                    court.court_code,
                ]
            )

if __name__ == '__main__':
    ecourts()
