#! /usr/bin/env python3
# Echo server program
import os
import socket
import threading
import time
import re
class EchoThread(threading.Thread):
    def __init__(self, conn, addr, server):
        super(EchoThread, self).__init__()
        #threading.Thread.__init__(self)
        self.s = conn
        self.addr = addr
        self.server = server
        print('Connected by', addr)

    def run(self):
        data = self.s.recv(1024)
        s = data.decode()
        if s == 'Nanosim':
            self.s.sendall(b'SUCCESS')
        elif s == 'DVP' :
            self.s.sendall(b'SUCCESS')
        elif re.match(r'NewFeature@[0-9]+', s):
            data = s.plit('@')
            # create tokens in LmServer
            self.server.createTokens(10 * int(data[1]))
            self.s.sendall(b'SUCCESS')
        elif re.match(r'token@[0-9]+)', s):
            data = s.plit('@')
            token = self.server.getToken(int(data[1]))
            if token != None:
                self.s.sendall(token.encode())
            self.s.sendall(b'FAIL')
        elif re.match(r'validateToken@.+', s):
            data = s.split('@', 1)
            if self.server.validateToken(data[1]) :
               self.s.sendall(b'SUCCESS')
            self.server.sendall(b'FAIL')
        else:
            self.s.sendall(b'FAIL') 
        
class LmServer():
    HOST = ''
    PORT = 50007
    tokens = []
    def __init__(self, HOST = '', PORT = 50007):
        self.HOST = HOST
        self.PORT = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        while True:
            self.s.listen(1)
            conn, addr = self.s.accept()
            if conn != None :
                EchoThread(conn, addr, self).start()

    def createTokens(self, num):
        for i in range(num):
            token = ''.join(random.choice(string.ascii + string.digits) for _ in range(8))
            self.tokens.append(token)

    def getToken(self, i):
        if i < len(self.tokens) :
            return self.tokens[i]
        return None
    
    def validateToken(self, token):
        if token in self.tokens:
            return True
        return False
    def destroyTokens(self) :
        self.tokens = []
        
if __name__ == '__main__':
    a = os.environ.get('LM_SERVER')
    if a != None:
        hostPort = a.split('@')
        LmServer(hostPort[0], hostPort[1])
    else :
        LmServer()
    
            
'''        
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    if conn != None:
        EchoThread(conn, addr).start()
'''


        
