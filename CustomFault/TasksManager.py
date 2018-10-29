#! /depot/Python-3.5.2/bin/python
import os
import argparse
import threading
import json
import subprocess
import shlex
import re
from CustomFault.LicManager import LicManager
from utils.collectMachines import CollectMachines
from PyQt5.QtCore import QObject, pyqtSignal

class ReportManager():
    def __init__(self, jsonParser, tasksManager) :
        self.jsonParser = jsonParser
        self.tasksManager = tasksManager

    def execute(self):
        outdir = os.path.abspath(self.jsonParser['outdir'])
        self.fileName = outdir + '/' + self.jsonParser['outprefix'] + '.log'
        with open(self.fileName, 'w') as f:
            f.write('CustomFault \n')
            f.write('Jobs to run: {}\n'.format(self.tasksManager.jobsNum))
            f.write('Success Jobs: {}\n'.format(self.tasksManager.ok))
            f.write('Failed Jobs: {}\n'.format(self.tasksManager.errors))

class Executor(threading.Thread):
    def __init__(self, host, script, tasksManager, licManager, token = None):
        super(Executor, self).__init__()
        self.host = host
        self.script = script
        self.tasksManager = tasksManager
        self.licManager = licManager
        self.token = token
        m = re.compile(r'-o ([\w/]+)')
        self.success = False
        with open(self.script) as f:
            for line in f:
                a = m.search(line)
                if a:
                    self.logfile = a.group(1) + '.log'
                    break
                
    def run(self):
        task = self.script
        if self.token:
            task = task + ' ' + self.token
        if self.host:
            task = 'rsh ' + self.host + ' ' + task
        p = subprocess.Popen(shlex.split(task))
        p.wait()
        m = re.compile(r'SUCCESS')
        with open(self.logfile) as f:
            for line in f:
                if m.match(line):
                    self.success = True

class TasksManager(QObject):
    dataChanged = pyqtSignal()
    addJob = pyqtSignal(str, str, str)
    removeJob = pyqtSignal(str)
    def __init__(self, jsonParser, licManager, num = 100):
        super(TasksManager, self).__init__()
        self.jsonParser = jsonParser
        self.licManager = licManager
        self.jobsNum = jsonParser['cases_num']
        
        self.hosts = []
        self.tasks = []
        self.executors = []
        self.needToken = (licManager.getFeature() == 'NewFeature')
        self.lock =  threading.Lock()
        self.pending = self.jobsNum
        self.running = 0
        self.ok = 0
        self.errors = 0
        pass

    def pushExecutor(self, executor):
        with self.lock:
            self.executors.append(executor)
            self.pending -= 1
            self.running += 1
            self.dataChanged.emit()
            self.addJob.emit(executor.host, executor.script, executor.token)
            print('launch: rsh={0:3d} pending={1:3d} running={2:3d} ok={3:3d} errors={4:3d}'.format(self.hostsNum, self.pending, self.running, self.ok, self.errors), end='\r')
        
    def removeExecutor(self, executor):
        if executor.host :
            self.pushHost(executor.host)
        if executor.token :
            self.licManager.pushToken(executor.token)

        with self.lock:
            self.running -= 1
            if executor.success:
                self.ok += 1
            else :
                self.errors += 1
            if self.executors:
                self.executors.remove(executor)
            self.dataChanged.emit()
            self.removeJob.emit(executor.host)
            print('launch: rsh={0:3d} pending={1:3d} running={2:3d} ok={3:3d} errors={4:3d}'.format(self.hostsNum, self.pending, self.running, self.ok, self.errors), end='\r')


    def pushHost(self, host):
        with self.lock:
            self.hosts.append(host)

    def popHost(self):
        host = None
        with self.lock:
            if self.hosts:
                host = self.hosts.pop()
        return host

    def collectMachines(self):
        if 'dpconfig_file' in self.jsonParser.keys():
            self.hosts = CollectMachines(self.jsonParser['dpconfig_file']).execute()
            self.hostsNum = len(self.hosts)
            self.dataChanged.emit()
        
    def createWorkerScript(self, worker):
        outdir = os.path.abspath(self.jsonParser['outdir'])
        fileName = outdir + '/tmp/' + worker + '.sh'
        with open(fileName, 'w') as f:
            license = os.environ['LM_SERVER']
            xa = self.jsonParser['simulator']

            f.write('#! /bin/bash\n')
            f.write('export LM_SERVER=\'' + license + '\'\n')
            f.write('if [ $# -eq 0 ]\n')
            f.write('then\n')
            f.write('  ' + xa + ' -i ' + worker + ' -o ' + outdir + \
                    '/workers/' + worker + '\n')
            f.write('else\n')
            f.write('  ' + xa + ' -i ' + worker + ' -o ' + outdir + \
                    '/workers/' + worker + ' -t $1\n')
            f.write('fi\n')
        os.chmod(fileName, 0o755)
    
    def createTasks(self):
        outdir = os.path.abspath(self.jsonParser['outdir'])
        dirname = outdir + '/tmp'
        if (dirname != '') and (not os.path.exists(dirname)):
            os.makedirs(dirname)
        for i in range(self.jobsNum):
            worker = 'worker' + str(i)
            self.createWorkerScript(worker)
            command = os.path.abspath(self.jsonParser['outdir']) + '/tmp/' + \
                      worker + '.sh'
            self.tasks.append(command)

    def submitTasks(self):
        while self.tasks:
            host = self.popHost()
            if host:
                if self.needToken:
                    token = self.licManager.popToken()
                    if token:
                        task = self.tasks.pop()
                        executor = Executor(host, task, self, self.licManager, token)
                        self.pushExecutor(executor)
                        executor.start()
                else :
                    task = self.tasks.pop()
                    executor = Executor(host, task, self, self.licManager)
                    self.pushExecutor(executor)
                    executor.start()
            excludeExecutors = []
            for executor in self.executors:
                if not executor.is_alive():
                    excludeExecutors.append(executor)
            for executor in excludeExecutors:
                self.removeExecutor(executor)
        for executor in self.executors:
            executor.join()
        executors = self.executors.copy()
        for executor in executors:
            self.removeExecutor(executor)
            
    def execute(self):
        print('Collect machines')
        self.collectMachines()
        print('Create tasks')
        self.createTasks()
        print('Run tasks')
        self.submitTasks()
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CustomFault simulator')
    parser.add_argument('--json', '-j', type=str, required= True, \
                        help='json file')
    args = parser.parse_args()
    with open(args.json) as f:
        jP = json.load(f)
    licManager = LicManager(jP['license']['prod_name'], 
                            jP['license']['prod_version'], 
                            jP['license']['feature'], 
                            jP['license']['nlic'])
    tasksManager = TasksManager(jP, licManager, jP['cases_num'])
    reportManager = ReportManager(jP, tasksManager)
    tasksManager.execute()
    reportManager.execute()


