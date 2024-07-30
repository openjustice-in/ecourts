import re
from collections import OrderedDict

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
  args_str = re.search(r'\((.*)\)', js_call).group(1)
  args = [arg.strip() for arg in args_str.split(',')]

  # Convert arguments to typed values based on the signature
  typed_args = {}
  while signature:
    key, type_ = signature.popitem(last=False)
    arg = args.pop(0)
    if type_ == str:
      arg = arg.strip('\'"')  # Remove leading and trailing quotes
    try:
      typed_args[key] = type_(arg)
    except ValueError:
      raise ValueError(f"Invalid argument type for {arg}: expected {type_}")

  return typed_args

if __name__ == "__main__":
  js_call = "x(1,2,3, 'four',23.4)"
  signature = OrderedDict([('count', int), ('v', int), ('c', int), ('description', str), ('money', float)])
  result = parse_js_call(js_call, signature)
  import wat
  wat/result
