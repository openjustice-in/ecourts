from entities import Case
from entities import Court
from entities.party import Party
from captcha import CaptchaError

# TODO: The dict mappings should be dynamic
# based on the route called.
def parse_cases(raw_data: str) -> list[Case]:
    """Processes raw data and returns a list of case dictionaries.

    Args:
    raw_data: The input data string.

    Returns:
    A list of dictionaries, each representing a case.
    """

    starting_str = raw_data[0:15].upper()
    if "ERROR" in starting_str:
        raise ValueError("Got invalid result")
    if "INVALID CAPTCHA" in starting_str:
        raise CaptchaError("Invalid captcha")
    if len(raw_data) == 0:
        return []
        # Some of the fields are not used and unknown
        # 201700001112024
        # HCP/111/2024
        # SAIF DIN TH. MOHD SHABIR Versus UT OF J AND K TH. PRINCIPAL SECRETARY TO GOVERNMENT HOME DEPARTMENTJAMMU AND OTHERS
        # JKHC020042172024
        # 1
        # 126
        # Jammu Wing
        # 14b730df47b74eb805c08ed47753d39e22ace0707e6229cfa567223d4f07a96f
    for record_block in raw_data.split("##"):
        record_fields = record_block.split("~")
        if len(record_fields) < 8:
            continue

        case_type,r_year,r_no = record_fields[1].split("/")
        petitioner,respondent = [x.replace("<br/>", "").strip() for x in record_fields[2].split("Versus")]
        cnr = record_fields[3].strip()
        case_obj = Case(
            case_type = case_type,
            registration_number = f"{r_year}/{r_no}",
            petitioners = [Party(name=petitioner)],
            respondents = [Party(name=respondent)],
            cnr_number = cnr,

        )
        case_obj.token = record_fields[7]
        case_obj.case_number = record_fields[0]
        yield case_obj
