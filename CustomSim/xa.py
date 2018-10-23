#! /usr/bin/env python
import argparse
import time
import random 
import datetime
import sys

parser = argparse.ArgumentParser(description='xa simulator')
parser.add_argument('--token', '-t', metavar='token', type=str, \
                    required=True, help='token')
parser.add_argument('--output', '-o', metavar='prefix', type=str, \
                    required=True, help='prefix')
args = parser.parse_args()
token = args.token
if not scl_validate_token(args.token):
    sys.exit(1)
                    
print(datetime.datetime.now())
time.sleep(random.uniform(0.5, 1.5))
print(datetime.datetime.now())
sys.exit(random.ranint(0,1))
