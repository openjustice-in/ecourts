from entities import Order
from entities import Court


# TODO: The dict mappings should be dynamic
# based on the route called.
def parse_orders(raw_data: str) -> list[Order]:
    """Processes raw data and returns a list of case dictionaries.

    Args:
    raw_data: The input data string.

    Returns:
    A list of dictionaries, each representing a case.
    """

    data_parts = raw_data.split("^^")
    if "ERROR" in data_parts[0].upper() or "INVALID CAPTCHA" in data_parts[0].upper():
        raise ValueError("Got invalid result")
    if len(raw_data) == 0:
        return []
    for record_block in data_parts[0].split("##"):
        record_fields = record_block.split("~")
        if len(record_fields) < 10:
            continue

        if (
            record_fields[7] == "Y"
            or record_fields[7] == "y"
            or record_fields[5] != "@#"
            or record_fields[6] != ""
        ):
            raise NotImplementedError()

        # TODO: Switch to returning a case with the orders= set instead
        yield Order(
            # court=Court(record_fields[9], record_fields[4]),
            # case_number=record_fields[0],
            date=record_fields[1],
            filename=record_fields[2],
            judgement="JUDGEMENT" in record_fields[3],
            # cino=record_fields[8],
        )
