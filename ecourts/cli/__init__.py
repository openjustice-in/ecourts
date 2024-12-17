import click
import csv
import sys
from entities import Court
from ecourt import ECourt, RetryException
from sys import stdout
from datetime import datetime
from storage import Storage
from tabulate import tabulate
import click
from functools import wraps
from parsers.cases import parse_cases

def validate_year(ctx, _, value):
    if value and (value < 1990 or value > 2025):
        raise click.BadParameter("Year must be in YYYY format")
    return value


def validate_date(ctx, _, value):
    if value:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise click.BadParameter("Date must be in YYYY-MM-DD format")
    return value


def setup_state_code(ctx, _, value):
    ctx.obj["state_code"] = value


def setup_court_code(ctx, _, value):
    ctx.obj["court"] = Court(state_code=ctx.obj["state_code"], court_code=value)


def common_options(f):
    @click.option("--case-number", help="Case number")
    @click.option("--party-name", help="Party name")
    @click.option("--case-type", type=int, help="Case type")
    @click.option("--year", callback=validate_year, type=int, help="Year in YYYY format")
    @click.option(
        "--state-code",
        callback=setup_state_code,
        help="State code of the Court",
        required=True,
    )
    @click.option(
        "--court-code", callback=setup_court_code, help="Court code of the Court"
    )
    @click.pass_context
    @wraps(f)
    def wrapper(ctx, *args, **kwargs):
        ctx.ensure_object(dict)
        for option in ["case_number", "party_name", "case_type", "year"]:
            if option in kwargs:
                ctx.obj[option] = kwargs[option]

        if not "court" in ctx.obj:
            raise click.BadParameter("A valid state-code, court-code is required")
        return f(*args, **kwargs)

    return wrapper


@click.group()
@click.pass_context
def ecourts(ctx):
    """eCourts application for retrieving case information."""
    ctx.ensure_object(dict)


@ecourts.command()
@common_options
@click.option("--fir-number", help="FIR number")
@click.option("--filing-number", help="Filing number")
@click.option(
    "--status", type=click.Choice(["Pending", "Disposed"]), help="Case status"
)
@click.option("--police-station-id", help="Police station ID")
@click.option("--act-type", help="ACT Type (number)")
@click.option("--save", help="Save cases to database", is_flag=True)
@click.pass_context
def get_cases(
    ctx,
    case_number,
    party_name,
    case_type,
    year,
    state_code,
    court_code,
    fir_number,
    filing_number,
    status,
    police_station_id,
    act_type,
    save
):
    court: Court = ctx.obj["court"]
    ecourt = ECourt(court)

    if case_number and case_type and year:
        ecourt.search_by_case_number(case_type, case_number, year)
    elif police_station_id:
        ecourt.search_by_fir_number(police_station_id, fir_number, year, status)
    elif party_name:
        ecourt.search_by_party_name(party_name, year, status)
    elif filing_number and year:
        ecourt.search_by_filing_number(filing_number, year)
    elif act_type != None and status != None:
        assert status != "Both"
        extra_fields = {
            "status": status,
            "act_type": act_type
        }
        cases = list(ecourt.ActType(act_type, status))
    elif case_type != None and status != None:
        assert status != "Both"
        extra_fields = {
            "status": status,
            "case_type_int": case_type
        }
        cases = list(ecourt.CaseType(case_type, status, year))
    else:
        click.echo(
            "Invalid combination of arguments. Please provide a valid set of options."
        )
        sys.exit(1)

    idx = 0
    for case in cases:
        res = {}
        fields = ['registration_number', 'cnr_number', 'name']
        for field in fields:
            value = getattr(case, field)
            if value:
                res[field] = value

        writer = csv.DictWriter(stdout, fieldnames=fields)
        if idx == 0:
            writer.writeheader()
        writer.writerow(res)
        idx += 1

    if save:
        print(court)
        print(cases)
        print(extra_fields)
        Storage().addCases(court, cases, extra_fields)


@ecourts.command()
@common_options
@click.option("--filing-number", help="Filing number")
@click.option(
    "--from-date", callback=validate_date, help="From date in YYYY-MM-DD format"
)
@click.option("--to-date", callback=validate_date, help="To date in YYYY-MM-DD format")
@click.pass_context
def get_orders(
    ctx,
    case_number,
    party_name,
    case_type,
    year,
    state_code,
    court_code,
    filing_number,
    from_date,
    to_date,
):
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
        click.echo(
            "Invalid combination of arguments. Please provide a valid set of options."
        )


@ecourts.command()
@click.option("--state-code", help="State code of the Court")
@click.option("--court-code", help="Court code of the Court")
@click.option("--save", help="Save data in database", is_flag=True)
@click.pass_context
def get_case_types(ctx, state_code, court_code, save):
    if state_code == None and court_code == None:
        courts = Court.enumerate()
    else:
        courts = [Court(state_code=state_code, court_code=court_code)]

    for court in courts:
        ecourt = ECourt(court)
        types = ecourt.getCaseTypes()
        if save:
            Storage().addCaseTypes(types)


@ecourts.command()
@click.option("--state-code", help="State code of the Court")
@click.option("--court-code", help="Court code of the Court")
@click.option("--save", help="Save data in database", is_flag=True)
@click.pass_context
def get_act_types(ctx, state_code, court_code, save):
    if state_code == None and court_code == None:
        courts = Court.enumerate()
    else:
        courts = [Court(state_code=state_code, court_code=court_code)]

    for court in courts:
        ecourt = ECourt(court)
        types = ecourt.getActTypes()
        if save:
            Storage().addActTypes(types)


@ecourts.command()
@click.option("--state-code", help="State code of the Court")
@click.option("--court-code", help="Court code of the Court")
@click.option("--date", help="Cause List Date", type=click.DateTime(formats=["%Y-%m-%d"]),
              default=str(datetime.today().date()))
@click.option("--save", help="Save data in database", is_flag=True)
@click.option("--max-attempts", help="Maximum attempts to make per court, in case of any errors", type=int, default=15)
@click.pass_context
def get_cause_lists(ctx, state_code, court_code, date: click.DateTime, save, max_attempts):

    if state_code == None and court_code == None:
        courts = list(Court.enumerate())
    else:
        courts = [Court(state_code=state_code, court_code=court_code)]

    for court in courts:
        ecourt = ECourt(court)
        ecourt.set_max_attempts(max_attempts)
        try:
            data = list(ecourt.getCauseLists(date.date()))
            if len(data) > 0:
                print(tabulate([
                    {"State": court.state_code, "Court": court.court_code} | cl.printable_dict()
                    for cl in data
                ], headers={"bench": "Bench", "type": "Type"}, tablefmt="presto"))
        except RetryException:
            if len(courts) > 1:
                print(f"Error in court {court}. Ignoring")
                continue
            else:
                raise


@ecourts.command()
@click.option("--cnr", help="Case CNR", required=False, type=str)
@click.option("--download-orders", help="Download Orderss", required=False, is_flag=True, default=False)
def enrich_cases(cnr, download_orders):
    s = Storage()
    for case_data in s.getCases():
        if cnr:
            if case_data['cnr_number'] != cnr:
                continue
        # cnr given = automatically force an update
        if case_data['case_status'] != None and cnr == None:
            continue
        
        court = Court(state_code=case_data['state_code'], court_code=case_data['court_code'])

        if 'case_type_int' not in case_data:
            case_data['case_type_int'] = s.findCaseType(court, case_data['case_type'])
            if case_data['case_type_int'] == None:
                print("Case Type not found for " + case_data['cnr_number'])
                continue

        ecourt = ECourt(court)
        registration_number = case_data['registration_number']
        # Search using case_type_int for now, we can move to number search, but that is heuristic really.
        cases = list(parse_cases(ecourt.searchSingleCase(registration_number, case_data['case_type_int'])))
        if len(cases) != 1:
            print("Error in parsing case " + case_data['cnr_number'] + " Got " + str(len(cases)) + " cases while searching")
        else:
            single_case = cases[0]
            new_case = ecourt.expand_case(single_case)
            if new_case.registration_number != single_case.registration_number or registration_number != single_case.registration_number:
                print("Case Details Mismatch" + case_data['cnr_number'])
            print(f"{new_case.cnr_number},{new_case.filing_number},{new_case.registration_number} {len(new_case.hearings)} Hearings, {len(new_case.orders)} Orders")
            s.addCases(ecourt.court, [new_case])

            if download_orders:
                if new_case.orders:
                    for order in new_case.orders:
                        fn = urllib.parse.quote_plus(order.filename)
                        if os.path.exists(f"orders/{fn}.pdf"):
                            continue
                        ecourt.downloadOrder(order, new_case, f"orders/{fn}.pdf")


@ecourts.command()
def stats():
    """Print statistics about the database."""
    stats = Storage().stats()
    for k, v in stats.items():
        click.echo(f"{k}: {v}")


if __name__ == "__main__":
    ecourts()
