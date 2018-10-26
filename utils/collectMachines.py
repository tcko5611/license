#! /depot/Python-3.5.2/bin/python
 
## @package  CollecMachines return a usable machines list

## $@class Main class
#  Use CollectMachine()
import os
import subprocess
import threading

class CollectMachines():
    def __init__(self, fileName):
        self.fileName = fileName
        self.hosts = []
        self.lock = threading.Lock()
        self.threads = []
        
    def execute(self):
        with open(self.fileName) as f:
            for host in f:
                host = host.strip()
                if host:
                    thread = threading.Thread(target=self.addTest, args = (host,))
                    self.threads.append(thread)
                    thread.start()
            for thread in self.threads:
                thread.join()
        return self.hosts

    def addTest(self, host):
        response = os.system("ping -c 1 " + host + '> /dev/null 2>&1')
        if response != 0 :
            return False
        
        command = ['/usr/bin/rsh', host, 'ls', '>/dev/null']
        process = subprocess.Popen(command)
        process.wait(timeout=10)
        process.kill()
        if process.returncode != 0 :
            return False
    
        command = os.environ['PYTHONPATH'] + '/utils/isAmd64.py'
        process = subprocess.Popen(['/usr/bin/rsh', host , command], stdout = subprocess.PIPE)
        process.wait()
        OK = process.stdout.readline().decode().strip()
        if OK == 'OK' :
            with self.lock:
                self.hosts.append(host)
            return True
        return False        
if __name__ == '__main__':
    p = CollectMachines('hosts')
    hosts = p.execute()
    print (hosts)
    
                
