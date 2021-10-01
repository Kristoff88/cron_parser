from src.parse_cron import parse_cron


def test_given_less_substrings__reports_error():
  assert parse_cron(" ")          == "Missing substrings: ['minute', 'hour', 'day of month', 'month', 'day of week', 'command']"
  assert parse_cron("0 ")         == "Missing substrings: ['hour', 'day of month', 'month', 'day of week', 'command']"
  assert parse_cron("0 0 ")       == "Missing substrings: ['day of month', 'month', 'day of week', 'command']"
  assert parse_cron("0 0 0 ")     == "Missing substrings: ['month', 'day of week', 'command']"
  assert parse_cron("0 0 0 0 ")   == "Missing substrings: ['day of week', 'command']"
  assert parse_cron("0 0 0 0 0 ") == "Missing substrings: ['command']"


def test_given_zeros__returns_zeros():
  assert parse_cron("0 0 0 0 0 /some_command --with-param; /some_other_command && /yet_another_command") == """
minute        0
hour          0
day of month  0
month         0
day of week   0
command       /some_command --with-param; /some_other_command && /yet_another_command
"""
