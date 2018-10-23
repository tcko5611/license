#! /usr/bin/env python3

# Echo server program
import argparse
import os
import socket
import threading
import time
import re
import random
import string
from utils.Singleton import Singleton

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
            self.s.sendall(b'SUCCESS')
        elif s == 'DVP' :
            self.s.sendall(b'SUCCESS')
        elif re.match(r'NewFeature@[0-9]+', s):
            data = s.split('@')
            # create tokens in LmServer
            self.server.createTokens(10 * int(data[1]))
            self.s.sendall(b'SUCCESS')
        elif re.match(r'token@[0-9]+', s):
            data = s.split('@')
            token = self.server.getToken(int(data[1]))
            if token != None:
                self.s.sendall(token.encode())
            else:
                self.s.sendall(b'FAIL')
        elif re.match(r'validateToken@.+', s):
            data = s.split('@', 1)
            if self.server.validateToken(data[1]) :
               self.s.sendall(b'SUCCESS')
            else:
                self.s.sendall(b'FAIL')
        else:
            self.s.sendall(b'FAIL') 
        
class LmServer(metaclass = Singleton):
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
            for i in range(num):
                token = ''.join(random.choice(string.ascii_letters + \
                                              string.digits) for _ in range(8))
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
    parser = argparse.ArgumentParser(description='star LM server')
    parser.add_argument('--host', metavar='host', type=str, required=True,
                        help='host name')
    parser.add_argument('--port', metavar='port', type=int, required=True,
                        help='port number')
    
    args = parser.parse_args()
    LmServer(args.host, args.port)



        
