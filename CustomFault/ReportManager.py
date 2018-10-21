class ReportManager():
    def __init__(self, tasksNum):
        self.total = tasksNum
        self.pending = tasksNum
        self.running = 0
        self.finished = 0
        self.lock = threading.Lock()
        pass
    def updateRunTask(self. taskName):
        with self.lock:
            self.pending -= 1
            self.running += 1
        pass
    def updateFinishTask(self, taskName):
        with self.lock:
            self.running -= 1
            self.finished += 1
        pass
    def report(self):
        pass
