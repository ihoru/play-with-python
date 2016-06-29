#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from time import time
from tools import eprint
from calculator import Calculator

start_rating = 500

parser = argparse.ArgumentParser(description='Calculate users\' rating after fights.')
parser.add_argument("-r", "--rating", type=int, dest="start_rating", default=start_rating,
                    help="Starting rating for users (default: %(default)s).")
parser.add_argument("-l", "--limit", type=int, dest="limit", default=10,
                    help="Number of users to read from file (default: %(default)s).")
parser.add_argument("-f", "--fights", type=int, dest="fights", default=1,
                    help="Number of fights to calculate (default: %(default)s).")
parser.add_argument("--file", type=argparse.FileType('r'), dest="file", default='users.txt',
                    help="Source file with data line-by-line: 'uid\\tmight' (default: %(default)s).")

args = parser.parse_args()
start_rating = args.start_rating > 0 and args.start_rating or 500
limit = args.limit > 0 and args.limit or 10000000
fights = args.fights > 0 and args.fights or 1
file = args.file
eprint(args)

calc = Calculator()
calc.read(file, start_rating, limit)
start = time()
calc.process(fights)
finish = time()
calc.print()

eprint('%.5f sec' % (finish - start))
