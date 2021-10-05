# cron_parser
The script takes a cron expression and prints out unwound schedule.

# Using application
No additional packages are required. Simply run the script:
`python src/main.py "*/15 0 1,15 * 1-5 /usr/bin/find"

minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find`

As of right now there is no installation mechanism.

# Running tests
Install dependencies via pip (it's good to use virtualenv).
`pip install -r requirements.txt`

Run tests in root dir.
`pytest`
