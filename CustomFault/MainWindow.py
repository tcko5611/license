#! /depot/Python-3.5.2/bin/python
import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from Ui_mainwindow import Ui_MainWindow
from CustomFault.LicManager import LicManager
from CustomFault.TasksManager import TasksManager, ReportManager

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.jsonButton.clicked.connect(self.loadJsonFile)
        self.runButton.clicked.connect(self.run)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['host', 'job'])
        self.tableWidget.horizontalHeader().setStretchLastSection(True);

    def loadJsonFile(self):
        fn, fileType = QFileDialog.getOpenFileName(self, 'Open File', None, 'Json files (*.json)')
        self.jsonLineEdit.setText(fn)
        self.rshLineEdit.setText('')
        self.pendingLineEdit.setText('')
        self.runningLineEdit.setText('')
        self.okLineEdit.setText('')
        self.errorsLineEdit.setText('')
        self.plainTextEdit.clear()


    def run(self):
        global app
        self.jsonButton.setEnabled(False)
        self.runButton.setEnabled(False)
        app.processEvents()
        self.statusbar.showMessage('Loading json file')
        jsonFile = self.jsonLineEdit.text()
        with open(jsonFile) as f:
            self.jP = json.load(f)
        self.statusbar.showMessage('Checkout License')
        self.licManager = LicManager(self.jP['license']['prod_name'], \
                                     self.jP['license']['prod_version'],\
                                     self.jP['license']['feature'], \
                                     self.jP['license']['nlic'])
        self.statusbar.showMessage('Prepare execute jobs')
        self.tasksManager = TasksManager(self.jP, self.licManager,
                                         self.jP['cases_num'])
        self.reportManager = ReportManager(self.jP, self.tasksManager)
        self.tasksManager.dataChanged.connect(self.dataChanged)
        self.tasksManager.addJob.connect(self.addTableJob)
        self.tasksManager.removeJob.connect(self.removeTableJob)
        self.statusbar.showMessage('Collect machines')
        self.tasksManager.collectMachines()
        # prepare for tablewidget showing
        self.needToken = self.tasksManager.needToken
        if self.needToken:
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setHorizontalHeaderLabels(['host', 'token', 'job'])
            self.tableWidget.horizontalHeader().setStretchLastSection(True);
        else:
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setHorizontalHeaderLabels(['host', 'job'])
            self.tableWidget.horizontalHeader().setStretchLastSection(True);

        self.tableWidget.setRowCount(self.tasksManager.hostsNum)
        self.hostsId = {}
        hostsNum = self.tasksManager.hostsNum
        for i in range(hostsNum):
            host = self.tasksManager.hosts[hostsNum - i -1]
            self.hostsId[host] = i
            self.tableWidget.setItem(i, 0, QTableWidgetItem(host)) 
        self.statusbar.showMessage('Create tasks')
        self.tasksManager.createTasks()
        self.progressBar.setRange(0, self.tasksManager.jobsNum)
        self.progressBar.setValue(0)
        self.statusbar.showMessage('Run tasks')
        self.tasksManager.submitTasks()
        while len(self.tasksManager.executors) != 0:
            pass
        print()
        self.statusbar.showMessage('Create report')
        self.reportManager.execute()
        self.proceedReport()
        self.statusbar.showMessage('Finished')

        self.jsonButton.setEnabled(True)
        self.runButton.setEnabled(True)
        app.processEvents()

    def proceedReport(self):
        with open(self.reportManager.fileName, 'r') as f:
            for line in f:
                self.plainTextEdit.appendPlainText(line)
                
    def dataChanged(self):
        global app
        self.rshLineEdit.setText(str(self.tasksManager.hostsNum))
        self.pendingLineEdit.setText(str(self.tasksManager.pending))
        self.runningLineEdit.setText(str(self.tasksManager.running))
        self.okLineEdit.setText(str(self.tasksManager.ok))
        self.errorsLineEdit.setText(str(self.tasksManager.errors))
        self.progressBar.setValue(self.tasksManager.jobsNum - \
                                  self.tasksManager.pending)
        app.processEvents()

    def addTableJob(self, host, job, token):
        global app
        i = self.hostsId[host]
        if self.needToken:
            self.tableWidget.setItem(i, 1, QTableWidgetItem(token)) 
            self.tableWidget.setItem(i, 2, QTableWidgetItem(job)) 
            pass
        else:
            self.tableWidget.setItem(i, 1, QTableWidgetItem(job)) 
        app.processEvents()

    def removeTableJob(self, host):
        global app
        i = self.hostsId[host]
        self.tableWidget.setItem(i, 1, QTableWidgetItem(''))
        if self.needToken:
            self.tableWidget.setItem(i, 2, QTableWidgetItem(''))
        app.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    import argparse
    parser = argparse.ArgumentParser(description='fault_sim_gui_json')
    parser.add_argument('-config', metavar='configfile', type=str, \
                        required=False, help='fault simulation gui configuration JSON file')
    
    args = parser.parse_args()
    mainWindow = MainWindow()
    
    mainWindow.show()
    sys.exit(app.exec_())
