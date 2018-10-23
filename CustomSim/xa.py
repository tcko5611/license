#! /usr/bin/env python
import argparse
import time
import random 
import datetime
import sys
import os
from SclApis.SclApis import *

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
dirname = os.path.dirname(prefix)
basename = os.path.basename(prefix)
if dirname and not os.path.exists(dirname):
    os.makedirs(basename)
    
time.sleep(random.uniform(0.5, 1.5))
print(datetime.datetime.now())

ret = random.ranint(0,1)
outName = args.output + '.log'
with open(outName, 'w') as f:
    if ret == 0:
        f.write(args.input + 'SUCESS')
    else:
        f.write(args.input + 'FAIL')
        
sys.exit(ret)
