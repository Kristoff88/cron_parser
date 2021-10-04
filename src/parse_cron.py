
class CronStringError(Exception):
  pass


def parse_cron(cron_str):
  substrings = [x for x in cron_str.split(' ') if x]
  __check_substring_count(substrings)

  minute, hour, day_of_month, month, day_of_week = substrings[:5]
  command = " ".join(substrings[5:])

  minute       = __parse_substring(minute,       "Minute",       0, 59)
  hour         = __parse_substring(hour,         "Hour",         0, 23)
  day_of_month = __parse_substring(day_of_month, "Day of month", 1, 31)
  month        = __parse_substring(month,        "Month",        1, 12)
  day_of_week  = __parse_substring(day_of_week,  "Day of week",  0, 6)

  return """
minute        {}
hour          {}
day of month  {}
month         {}
day of week   {}
command       {}
""".format(minute, hour, day_of_month, month, day_of_week, command)


def __check_substring_count(substrings):
  EXPECTED_SUBSTRINGS = ['minute', 'hour', 'day of month', 'month', 'day of week', 'command']
  MINIMAL_SUBSTRINGS_COUNT = len(EXPECTED_SUBSTRINGS)

  num_of_substrings = len(substrings)

  if num_of_substrings < MINIMAL_SUBSTRINGS_COUNT:
    raise CronStringError("Missing substrings: {}".format(EXPECTED_SUBSTRINGS[num_of_substrings:]))


def __parse_substring(substr, name, min_value, max_value):
  unwound_expression = substr

  if substr == '*':
    unwound_expression = __unwind_range(min_value, max_value)

  elif '-' in substr:
    lower_bound, upper_bound = substr.split('-')
    unwound_expression = __unwind_range(int(lower_bound), int(upper_bound))

  elif int(substr) < min_value or int(substr) > max_value:
    raise CronStringError("{} {} outside of range {}-{}!".format(name, int(substr), min_value, max_value))

  return unwound_expression


def __unwind_range(min_value, max_value):
  return ' '.join(str(x) for x in range(min_value, max_value+1))

