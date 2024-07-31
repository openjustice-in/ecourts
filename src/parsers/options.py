def parse_options(raw_input):
    """Options<Select> for HTML

    Args:
      n: A string response from the API

    Returns:
      A dictionary where keys are the first part of each option and values are
      the second part. Values with keys 'D' are marked as disabled.
    """

    result = {}
    options = n.split("#")
    for option in options:
        if option:
            key, value = option.split("~")
            result[key] = {"value": value, "disabled": key == "D"}
    return result
