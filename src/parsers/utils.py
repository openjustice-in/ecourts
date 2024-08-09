from collections import OrderedDict
import datetime
from typing import Optional
import re


def parse_js_call(js_call, signature):
    """
    Parses a JavaScript function call and returns a dictionary of typed arguments.

    Args:
      js_call: The JavaScript function call as a string.
      signature: An OrderedDict mapping argument names to their types.

    Returns:
      A dictionary of typed arguments.
    """

    # Extract arguments from the JavaScript function call
    args_str = re.search(r"\((.*)\)", js_call).group(1)
    args = [arg.strip() for arg in args_str.split(",")]

    # Convert arguments to typed values based on the signature
    typed_args = {}
    while signature:
        key, type_ = signature.popitem(last=False)
        arg = args.pop(0)
        arg = arg.strip("'\"")  # Remove leading and trailing quotes
        try:
            typed_args[key] = type_(arg)
        except ValueError:
            raise ValueError(f"Invalid argument type for {arg}: expected {type_}")

    return typed_args


def parse_date(date_str: Optional[str]) -> Optional[datetime.date]:
    if not date_str:
        return None
    date_formats = [
        "%Y%m%d",
        "%d-%m-%Y",
        "%dth %B %Y",
        "%dst %B %Y",
        "%dnd %B %Y",
    ]
    for fmt in date_formats:
        try:
            x = datetime.datetime.strptime(date_str, fmt).date()
            if x.year < 2050:
                return x
        except ValueError:
            pass
    return None


def _remove_all_attrs_except_saving(soup):
    for tag in soup.find_all(True):
        for attr in dict(tag.attrs):
            if attr not in ["href", "onclick", "id", "class"]:
                del tag.attrs[attr]
    return soup


def clean_html(soup) -> str:
    soup = _remove_all_attrs_except_saving(soup)
    soup = soup.select_one("body")
    # for tag in soup.find_all('br'):
    #     tag.decompose()
    return str(soup)
