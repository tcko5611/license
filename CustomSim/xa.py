#! /depot/Python-3.5.2/bin/python
import argparse
from SclApis.SclApis import *
import time
import random
import sys
import os

if __name__ == '__main__':
    # print (time.ctime())
    parser = argparse.ArgumentParser(description='xa simulator')
    parser.add_argument('--token', '-t', type=str, help='token for server')
    parser.add_argument('--output', '-o', type=str, required=True, help='output file prefix')
    parser.add_argument('--input', '-i', type=str, required=True, help='input')
    args = parser.parse_args()
    if args.token:
        #print("LM_SERVER" + os.environ['LM_SERVER'])
        ret = scl_lc_validate_token(args.token)
        if not ret :
            print('Failed validate token, exit')
            sys.exit(1)
    else:
        ret = scl_lc_checkout('', 'CustomSim_Beta', '', 1, 0, '', 0)
        if not ret:
            print('Failed check out license, exit')
            sys.exit(1)
            
    dirname = os.path.dirname(args.output)
    if (dirname != '') and (not os.path.exists(dirname)):
        try :
            os.makedirs(dirname)
        except FileExistsError:
            print (dirname + ' directory exists')
    # print(os.path.basename(args.output))

    outFileName = args.output + '.log'
    ret = random.randint(0, 1)
    with open(outFileName, 'w') as f:
        f.write(args.input + ' has Done\n')
        if ret == 0:
            f.write('SUCCESS\n')
        else:
            f.write('FAIL\n')
        f.flush()
    t = random.uniform(0.5, 1.5)
    time.sleep(t)
    sys.exit(ret)
