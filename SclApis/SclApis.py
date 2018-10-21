#! /usr/bin/env python3
import os
import threading
import socket
#from SclApis import *

def scl_checkout(feature, nlic):
    if feature == 'DVP':
        return True
    elif feature == 'Nanosim':
        return True
    elif feature == 'NewFeature' :
        host = 'ktc-PC'
        port = 50007
        a = os.environ.get('LM_SERVER')
        if a != None:
            hostPort = a.split('@')
            host = hostPort[0]
            port = int( hostPort[1])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            data = 'NewFeature@' + str(nlic)
            s.sendall(data.encode())
            data = s.recv(1024)
            ret = data.decode()
            if ret == 'SUCCESS' :
                return True
    return False

def scl_checkin(feature):
    return True

def scl_get_token(i):
    host = 'ktc-PC'
    port = 50007
    a = os.environ.get('LM_SERVER')
    if a != None:
        hostPort = a.split('@')
        host = hostPort[0]
        port = int( hostPort[1])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = 'token@' + str(i)
        s.sendall(data.encode())
        data = s.recv(1024)
        ret = data.decode()
        if ret == 'FAIL' :
            return None
        else :
            return ret
    return None

def scl_validate_token(token):
    host = 'ktc-PC'
    port = 50007
    a = os.environ.get('LM_SERVER')
    if a != None:
        hostPort = a.split('@')
        host = hostPort[0]
        port = int( hostPort[1])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = 'validateToken@' + token
        s.sendall(data.encode())
        data = s.recv(1024)
        ret = data.decode()
        if ret == 'SUCCESS' :
            return True
    return False

def runLmServer():
    LmServer()

if __name__ == '__main__' :
    os.environ['LM_SERVER'] = 'tcko-PC@50008'
    from LmServer import LmServer
    t = threading.Thread(target = runLmServer)
    t.start()

    print(scl_checkout('SomeKey', 1))
    print(scl_checkout('DVP', 2))
    print(scl_checkout('Nanosim', 2))

    print(scl_checkout('NewFeature', 2))
    for i in range(20):
        print(scl_get_token(i))
    print(scl_get_token(21))
    token = scl_get_token(19)
    print(token)
    print(scl_validate_token(token))
