#! /depot/Python-3.5.2/bin/python

import subprocess
import sys
import os

p = subprocess.Popen(['uname', '-s'], stdout=subprocess.PIPE)
OS = p.stdout.readline().decode().strip()
p.wait()
p.stdout.close()
p = subprocess.Popen(['uname', '-m'], stdout=subprocess.PIPE)
machine = p.stdout.readline().decode().strip()
p.wait()
p.stdout.close()
if OS == 'Linux' and machine == 'x86_64' and not os.path.isfile('/etc/SuSE-release') :
    print('OK')
    sys.exit(1)
else:
    print('')
    sys.exit(0)
