#! /depot/Python-3.5.2/bin/python
import sys
import os
import re
def get_cpu():
    cpuinfos = []
    cpu_total = 0
    cpu_speed = 0
    p = re.compile("cpu[ \t]+[mM][hH][zZ][ \t]*(:[ \t]*)?([0-9]+(\.[0-9]*)?)")
    cmd = 'grep -i "cpu mhz" /proc/cpuinfo'
    for line in  os.popen(cmd).readlines():
        line = line[:-1]
        m = p.match(line)
        if m:
            cpu_total += 1
            cpu_speed = cpu_speed + float(m.group(2))
#            print m.group(2)
        cpuinfos.append(line)
#    for line in cpuinfos:

    cpu_speed /= cpu_total
#    print cpu_speed
#    print cpu_total
    return [cpu_total, cpu_speed]

# main program
[cpu_total, cpu_speed] = get_cpu()
#print cpu_total, cpu_speed
x=[]
cmd = 'vmstat 1 2'
x = os.popen(cmd).readlines()
key = []
dat = []
key = x[1].split()
dat = x[3].split()
vmMap = {}
for q, a in zip(key, dat):
    vmMap[q] = a
if not ('free' in vmMap.keys()) or not ('id' in vmMap.keys()):
    print ("Unexpected format in vmwait")
    sys.exit(1)
    
mem_free  = float(vmMap["free"]) / 1024.0;
cpu_idle =  float(vmMap["id"]) * float(cpu_total) * 0.01;
print ("cpu_free=%.1f cpu_speed=%.0fMHz mem_free=%.0fMB" % (cpu_idle, cpu_speed, mem_free))
