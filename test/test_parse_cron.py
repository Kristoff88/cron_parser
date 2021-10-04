import pytest

from src.parse_cron import parse_cron, CronStringError


def test_given_less_substrings__raises_error():
  with pytest.raises(CronStringError) as err:
    parse_cron(" ")
  assert"Missing substrings: ['minute', 'hour', 'day of month', 'month', 'day of week', 'command']" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 ")
  assert"Missing substrings: ['hour', 'day of month', 'month', 'day of week', 'command']" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 ")
  assert"Missing substrings: ['day of month', 'month', 'day of week', 'command']" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 1 ")
  assert"Missing substrings: ['month', 'day of week', 'command']" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 1 1 ")
  assert"Missing substrings: ['day of week', 'command']" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 1 1 0 ")
  assert"Missing substrings: ['command']" in str(err.value)


def test_simple_values__within_range():
  assert parse_cron("0 0 1 1 0 /some_command") == """
minute        0
hour          0
day of month  1
month         1
day of week   0
command       /some_command
"""

  assert parse_cron("59 23 31 12 6 /some_command") == """
minute        59
hour          23
day of month  31
month         12
day of week   6
command       /some_command
"""


def test_simple_values__outside_range():
  with pytest.raises(CronStringError) as err:
    parse_cron("60 0 1 1 0 /some_command")
  assert"Minute 60 outside of range 0-59!" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 24 1 1 0 /some_command")
  assert"Hour 24 outside of range 0-23!" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 0 1 0 /some_command")
  assert"Day of month 0 outside of range 1-31!" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 32 1 0 /some_command")
  assert"Day of month 32 outside of range 1-31!" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 1 0 0 /some_command")
  assert"Month 0 outside of range 1-12!" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 1 13 0 /some_command")
  assert"Month 13 outside of range 1-12!" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 1 1 7 /some_command")
  assert"Day of week 7 outside of range 0-6!" in str(err.value)


def test_simple_values__star_expression():
  assert parse_cron("* * * * * /some_command") == """
minute        0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59
hour          0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
day of month  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   0 1 2 3 4 5 6
command       /some_command
"""


def test_complex_command():
  assert parse_cron("0 0 1 1 0 /some_command --with-param; /some_other_command && /yet_another_command") == """
minute        0
hour          0
day of month  1
month         1
day of week   0
command       /some_command --with-param; /some_other_command && /yet_another_command
"""
