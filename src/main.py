#import argparse
#
#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('minute', type=str, help='foo')
#parser.add_argument('hour', type=str, help='foo')
#parser.add_argument('day_of_month', type=str, metavar='day of month', help='foo')
#parser.add_argument('month', type=str, help='foo')
#parser.add_argument('day_of_week', type=str, metavar='day of week', help='foo')
#parser.add_argument('command', type=str, help='foo')
#
#args = parser.parse_args()
#
#print(args.minute)
#print(args.hour)
#print(args.day_of_month)
#print(args.month)
#print(args.day_of_week)
#print(args.command)


import sys

from parse_cron import parse_cron, CronStringError


assert len(sys.argv) == 2
cron_string = sys.argv[1]

try:
  print( parse_cron(cron_string) )
except CronStringError as err:
  print(err)
