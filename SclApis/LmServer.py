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
            print('Checkout Nanosim License')
            self.s.sendall(b'SUCCESS')
        elif s == 'DVP' :
            print('Checkout DVP License')
            self.s.sendall(b'SUCCESS')
        elif re.match(r'NewFeature@[0-9]+', s):
            data = s.split('@')
            # create tokens in LmServer
            # self.server.createTokens(10 * int(data[1]))
            print('Checkout NewFeature linces')
            self.s.sendall(b'SUCCESS')
        elif re.match(r'inittoken@[0-9]+', s):
            data = s.split('@')
            # create tokens in LmServer
            self.server.createTokens(int(data[1]))
            print('Init NewFeature tokens')
            self.s.sendall(b'SUCCESS')
        elif re.match(r'token@[0-9]+', s):
            data = s.split('@')
            i = int(data[1])
            token = self.server.getToken(i)
            if token != None:
                print('Send token ' + token + ' at ' + str(i))
                self.s.sendall(token.encode())
            else:
                print('Send token at ' + str(i) + ' FAIL')
                self.s.sendall(b'FAIL')
        elif re.match(r'validateToken@.+', s):
            # print(s)
            data = s.split('@', 1)
            # print(data[1])
            if self.server.validateToken(data[1]) :
                print('Valiadte Token ' + data[1] + ' SUCESS')
                self.s.sendall(b'SUCCESS')
            else :
                print('Valiadte Token ' + data[1] + ' FAIL')
                self.s.sendall(b'FAIL')
        else:
            print('UNKNOWN REQUEST')
            self.s.sendall(b'FAIL') 
        
class LmServer():
    tokens = []
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.lock = threading.Lock()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        while True:
            self.s.listen(1)
            conn, addr = self.s.accept()
            if conn != None :
                EchoThread(conn, addr, self).start()
 
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
    LmServer(args.host, args.port)
