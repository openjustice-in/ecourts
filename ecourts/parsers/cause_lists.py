from entities.cause_list import CauseList
from collections.abc import Iterator
from datetime import datetime


def parse_cause_lists(raw_data: str) -> Iterator[CauseList]:
    """Processes raw data and returns a list of all cause lists

    Args:
    raw_data: The input data string.

    Returns:
    A list of Cause Lists
    """

    data_parts = raw_data.split("^#")
    if "ERROR" in data_parts[0].upper() or "INVALID CAPTCHA" in data_parts[0].upper():
        raise ValueError("Got invalid result")
    if len(raw_data) == 0:
        return []
    for record_block in data_parts:
        record_fields = record_block.split("~")
        if len(record_fields) < 5:
            continue

        # TODO: There is a second URL for eliminated cause lists.
        # if (record_fields[5] == "Y"):
        #     raise NotImplementedError("Cause List was eliminated, and that is not yet implemented")

        assert (datetime.strptime(record_fields[8], "%Y-%m-%d") == datetime.strptime(record_fields[3], "%d-%m-%Y"))

        yield CauseList(
            bench=record_fields[1].strip(),
            type=record_fields[2].strip(),
            date=datetime.strptime(record_fields[8].strip(), "%Y-%m-%d").date(),
            filename=record_fields[4].strip(),
            eliminated=record_fields[5].strip() == "Y",
            bench_id=record_fields[6].strip(),
            causelist_id=record_fields[7].strip()
        )
