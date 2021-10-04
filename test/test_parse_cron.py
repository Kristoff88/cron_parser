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
    parse_cron("0 0 0 ")
  assert"Missing substrings: ['month', 'day of week', 'command']" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 0 0 ")
  assert"Missing substrings: ['day of week', 'command']" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_cron("0 0 0 0 0 ")
  assert"Missing substrings: ['command']" in str(err.value)


def test_given_zeros__returns_zeros():
  assert parse_cron("0 0 0 0 0 /some_command --with-param; /some_other_command && /yet_another_command") == """
minute        0
hour          0
day of month  0
month         0
day of week   0
command       /some_command --with-param; /some_other_command && /yet_another_command
"""
