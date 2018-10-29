#! /depot/Python-3.5.2/bin/python
import os
import sys
import json

# from SclApis.LmServer import LmServer

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QTextCursor
from Ui_mainwindow import Ui_MainWindow
from LmServer import LmServer

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.runButton.clicked.connect(self.run)
        self.cursor = QTextCursor(self.plainTextEdit.textCursor())
        
    def run(self):
        host = self.hostLineEdit.text()
        port = int(self.portLineEdit.text())
        self.lmServer = LmServer(host, port)
        self.lmServer.setDaemon(True)
        self.lmServer.sendMessage.connect(self.dataChanged)
        self.lmServer.start()
        self.plainTextEdit.appendPlainText('LM server started')
        
    def dataChanged(self, str1) :
        global app
        self.plainTextEdit.appendPlainText(str1)
        self.cursor.movePosition(QTextCursor.End)
        self.plainTextEdit.setTextCursor(self.cursor)
        app.processEvents()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    
    mainWindow.show()
    sys.exit(app.exec_())
