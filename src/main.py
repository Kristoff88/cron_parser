import argparse

from cron_string_error import CronStringError
from parse_cron import parse_cron


parser = argparse.ArgumentParser(
  description="Takes cron string and expands each field "
              "to show the times at which it will run."
)
parser.add_argument(
  'cron_string',
  type=str,
  help="cron string composed of minute, hour, day of "
       "month, month, and day of week"
)

args = parser.parse_args()

try:
  print( parse_cron(args.cron_string) )
except CronStringError as err:
  print(err)
