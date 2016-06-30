# Script usage
```
$ ./main.py -h
usage: main.py [-h] [--default-rating DEFAULT_RATING] [--percent PERCENT]
               [--limit LIMIT] [--fights FIGHTS] [--file FILE]

Calculate users' rating after fights.

optional arguments:
  -h, --help            show this help message and exit
  --default-rating DEFAULT_RATING
                        Default rating for users (default: 500).
  --percent PERCENT     Percent of user's current rating to find opponent
                        (default: 30).
  --limit LIMIT         Number of users to read from file (default: 10).
  --fights FIGHTS       Number of fights to calculate (default: 1).
  --file FILE           Source file with data line-by-line: 'uid\tmight'
                        (default: users.txt).
```
