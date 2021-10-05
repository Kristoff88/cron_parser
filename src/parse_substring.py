from cron_string_error import CronStringError


def parse_substring(substr, name, min_value, max_value):
  assert(min_value <= max_value)

  unwound_expression = substr

  if substr == '*':
    unwound_expression = __unwind_range(min_value, max_value)

  elif '-' in substr:
    lower_bound, upper_bound = list(map(int, substr.split('-')))
    __validate_range(substr, name, lower_bound, upper_bound, min_value, max_value)
    unwound_expression = __unwind_range(lower_bound, upper_bound)

  elif ',' in substr:
    values = list(map(int, substr.split(',')))
    unwound_expression = __unwind_list(values)

  elif '/' in substr:
    _, step = substr.split('/')
    unwound_expression = __unwind_range(min_value, max_value, int(step))

  elif int(substr) < min_value or int(substr) > max_value:
    raise CronStringError("{} {} outside of range {}-{}!".format(name, int(substr), min_value, max_value))

  return unwound_expression


def __unwind_range(min_value, max_value, step=1):
  return __unwind_list(range(min_value, max_value+1)[::step])


def __unwind_list(values):
  return ' '.join(str(x) for x in values)


def __validate_range(substr, name, lower_bound, upper_bound, min_value, max_value):
  if lower_bound < min_value:
    raise CronStringError("{} {} lower bound outside of range {}-{}!".format(name, lower_bound, min_value, max_value))

  if upper_bound > max_value:
    raise CronStringError("{} {} upper bound outside of range {}-{}!".format(name, upper_bound, min_value, max_value))

  if lower_bound > upper_bound:
    raise CronStringError("{} inverted range {}!".format(name, substr))
