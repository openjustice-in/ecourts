def parse_options(raw_input: str):
    """Options<Select> for HTML

    Args:
      n: A string response from the API

    Returns:
      A dictionary where keys are the first part of each option and values are
      the second part. Values with keys 'D' are marked as disabled.
    """

    result = []
    options = raw_input.split("#")
    for option in options:
        if option:

            try:
                key, value = option.split("~")
            except ValueError:
                key, value = option.split(";")
            result.append((key, value))
    return result
