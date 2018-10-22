#! /usr/bin/env python
import argparse
import time
import random 
import datetime
import sys

parser = argparse.ArgumentParser(description='xa simulator')
parser.add_argument('--token', '-t', metavar='token', type=str, required=True,
help='license token')
args = parser.parse_args()
token = args.token
print(datetime.datetime.now())
time.sleep(random.uniform(0.5, 1.5))
print(datetime.datetime.now())
sys.exit(5)
