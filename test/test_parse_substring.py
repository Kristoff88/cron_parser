import pytest

from cron_string_error import CronStringError
from parse_substring import parse_substring

pytestmark = pytest.mark.ut


def test_simple_values__within_range():
  assert parse_substring("0", "some_substr", 0, 1) == "0"
  assert parse_substring("1", "some_substr", 0, 1) == "1"


def test_simple_values__outside_range():
  with pytest.raises(CronStringError) as err:
    parse_substring("0", "some_substr", 1, 2)
  assert "some_substr 0 outside of range 1-2!" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_substring("3", "some_substr", 1, 2)
  assert "some_substr 3 outside of range 1-2!" in str(err.value)


def test_simple_values__star_expression():
  assert parse_substring("*", "some_substr", 1, 3) == "1 2 3"


def test_range_values__full_range():
  assert parse_substring("1-3", "some_substr", 1, 3) == "1 2 3"


def test_range_values__partial_range():
  assert parse_substring("2-3", "some_substr", 1, 4) == "2 3"


def test_range_values__single_element_range():
  assert parse_substring("1-1", "some_substr", 1, 1) == "1"


def test_range_values__outside_range():
  with pytest.raises(CronStringError) as err:
    parse_substring("0-1", "some_substr", 1, 2)
  assert "some_substr 0 lower bound outside of range 1-2!" in str(err.value)

  with pytest.raises(CronStringError) as err:
    parse_substring("2-3", "some_substr", 1, 2)
  assert "some_substr 3 upper bound outside of range 1-2!" in str(err.value)


def test_range_values__inverted_range():
  with pytest.raises(CronStringError) as err:
    parse_substring("2-1", "some_substr", 1, 2)
  assert "some_substr inverted range 2-1!" in str(err.value)


def test_sequence_values__full_sequence():
  assert parse_substring("1,2,3", "some_substr", 1, 3) == "1 2 3"


def test_sequence_values__partial_sequence():
  assert parse_substring("2,3", "some_substr", 1, 4) == "2 3"


def test_sequence_values__unordered_sequence():
  assert parse_substring("3,1,2", "some_substr", 1, 3) == "3 1 2"


def test_intervals():
  assert parse_substring("*/2", "some_substr", 1, 4) == "1 3"
  assert parse_substring("*/15", "some_substr", 0, 59) == "0 15 30 45"
  assert parse_substring("*/10", "some_substr", 1, 31) == "1 11 21 31"
