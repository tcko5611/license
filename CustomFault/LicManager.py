#! /usr/bin/env python3
import sys
import threading
from utils.Singleton import Singleton
from SclApis.SclApis import *

#class LicManager(metaclass = Singleton):
class LicManager():
    def __init__(self, feature, nlic):
        self.feature = None
        self.nlic = 0
        self.tokens = []
        self.availTokens = None
        self.checkouted = False
        self.lock = threading.Lock()
        
        if scl_checkout(feature, nlic):
            self.feature = feature
            self.nlic = nlic
            self.checkouted = True
        if feature == 'NewFeature':
            for i in range(10 * nlic):
                self.tokens.append(scl_get_token(i))
        self.availTokens = self.tokens[:]

    def getFeature(self):
        return self.feature

    def getNlic(self):
        return self.nlic
    
    def isCheckout(self):
        return self.checkouted

    def isAvailableTokens(self):
        with self.lock:
            if self.availTokens:
                return True
        return False

    def popToken(self):
        with self.lock:
            if self.availTokens:
                return self.availTokens.pop()
        return None

    def pushToken(self, token):
        with self.lock:
            if self.availTokens != None:
                if token in self.tokens and not (token in self.availTokens):
                    self.availTokens.append(token)
                    return True
        return False

def runLmServer():
    print('LM server start')
    LmServer()
    
if __name__ == '__main__' :
    os.environ['LM_SERVER'] = 'tcko-PC@50008'
    from SclApis.LmServer import LmServer
    threading.Thread(target = runLmServer, daemon = True).start()
    lic = LicManager('DVP', 2)
    print(lic.getFeature())
    lic = LicManager('Nanosim', 2)
    print(lic.isCheckout())
    
    lic = LicManager('NewFeature', 2)
    print(lic.isCheckout())
    i = 0
    tokens = []
    while lic.isAvailableTokens():
        token = lic.popToken()
        i += 1
        print('{:+d}: {}'.format(i, token))
        tokens.append(token)
    while tokens :
        token = tokens.pop()
        print('{}, {}'.format(token, scl_validate_token(token)))
    print('{}, {}'.format('aaa', scl_validate_token('aaa')))
