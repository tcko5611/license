#! /depot/Python-3.5.2/bin/python

# Echo server program
import argparse
import os
import socket
import threading
import time
import re
import random
import string
from PyQt5.QtCore import QObject, pyqtSignal

# from utils.Singleton import Singleton

class EchoThread(threading.Thread):
    def __init__(self, conn, addr, server):
        super(EchoThread, self).__init__()
        self.s = conn
        self.addr = addr
        self.server = server
        # print('Connected by', addr)

    def run(self):
        data = self.s.recv(1024)
        s = data.decode()
        if s == 'Nanosim':
            str1 = 'Checkout Nanosim License'
            self.server.setMessage(str1)
            self.s.sendall(b'SUCCESS')
        elif s == 'DVP' :
            str1 = 'Checkout DVP License'
            self.server.setMessage(str1)
            self.s.sendall(b'SUCCESS')
        elif re.match(r'NewFeature@[0-9]+', s):
            data = s.split('@')
            str1 = 'Checkout NewFeature lincens'
            self.server.setMessage(str1)
            self.s.sendall(b'SUCCESS')
        elif re.match(r'inittoken@[0-9]+', s):
            data = s.split('@')
            # create tokens in LmServer
            self.server.createTokens(int(data[1]))
            str1 = 'Init NewFeature tokens'
            self.server.setMessage(str1)
            self.s.sendall(b'SUCCESS')
        elif re.match(r'token@[0-9]+', s):
            data = s.split('@')
            i = int(data[1])
            token = self.server.getToken(i)
            if token != None:
                str1 = 'Send token ' + token + ' at ' + str(i)
                self.server.setMessage(str1)
                self.s.sendall(token.encode())
            else:
                str1 = 'Send token at ' + str(i) + ' FAIL'
                self.server.setMessage(str1)
                self.s.sendall(b'FAIL')
        elif re.match(r'validateToken@.+', s):
            # print(s)
            data = s.split('@', 1)
            # print(data[1])
            if self.server.validateToken(data[1]) :
                str1 = 'Valiadte Token ' + data[1] + ' SUCESS'
                self.server.setMessage(str1)
                self.s.sendall(b'SUCCESS')
            else :
                str1 = 'Valiadte Token ' + data[1] + ' FAIL'
                self.server.setMessage(str1)
                self.s.sendall(b'FAIL')
        else:
            str1 = 'UNKNOWN REQUEST'
            self.server.setMessage(str1)
            self.s.sendall(b'FAIL') 
        
class LmServer(QObject, threading.Thread):
    tokens = []
    sendMessage = pyqtSignal(str)

    def __init__(self, host, port, parent = None):
        super(LmServer, self).__init__(parent)
        self.HOST = host
        self.PORT = port
        self.lock = threading.Lock()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        
    def run(self):
        while True:
            self.s.listen(1)
            conn, addr = self.s.accept()
            if conn != None :
                EchoThread(conn, addr, self).start()
        
    def setMessage(self, str1) :
        with self.lock:
            print(str1)
            self.sendMessage.emit(str1)
            
    def createTokens(self, num):
        with self.lock:
            self.tokens = []
            for i in range(num):
                token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
                self.tokens.append(token)

    def getToken(self, i):
        with self.lock:
            if i < len(self.tokens) :
                return self.tokens[i]
        return None
    
    def validateToken(self, token):
        with self.lock:
            if token in self.tokens:
                return True
        return False

    def destroyTokens(self) :
        with self.lock:
            self.tokens = []
        
if __name__ == '__main__':
    # host : fsei317, port : 50008
    parser = argparse.ArgumentParser(description='star LM server')
    parser.add_argument('--host', metavar='host', type=str, required=True,
                        help='host name')
    parser.add_argument('--port', metavar='port', type=int, required=True,
                        help='port number')
    
    args = parser.parse_args()
    p = LmServer(args.host, args.port)
    print('LM Server started')
    p.start()
