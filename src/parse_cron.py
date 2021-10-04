
class CronStringError(Exception):
  pass


def parse_cron(cron_str):
  substrings = [x for x in cron_str.split(' ') if x]

  result = __check_substring_count(substrings)

  minute, hour, day_of_month, month, day_of_week = substrings[:5]
  command = " ".join(substrings[5:])

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
