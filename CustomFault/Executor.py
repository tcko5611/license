#! /usr/bin/env python3
import shlex
import subprocess
class Executor(threading.Thread):
    def __init__(self, host = '', command, token):
        self.host = host
        self.token = token
        self.command = shlex.split(command)
        self.taskManager = taskManager
        self.reportManager = reportManager
        self.isDone = True

    def run(self):
        process = subprocess.Popen(self.command)
        process.wait()
        self.isDone = True

    def isDone(self):
        return self.isDone

    def token(self):
        return self.token

    def host(self):
        return self.host
        
