#! /depot/Python-3.5.2/bin/python
# from utils.singleton import Singleton
import sys
import threading
from SclApis.SclApis import *

## Documentation for a class
#
# The LicManager is used to checkout license and manage tokens
class LicManager():
    ## The constructor, when checkout license fail will terminate the program
    # @param prodName The product name.
    # @param prodVersion The SRM version of the product.
    # @param feature The feature name to be checked out.
    # @param nlic The number of licenses to be checked out.
    def __init__(self, prodName, prodVersion, feature, nlic):
        self.prodName =  prodName
        self.prodVersion = prodVersion
        self.FC_KEY_MAXLEN = 64
        self.keyStr = feature
        self.verStr = prodVersion
        self.nlic = nlic
        self.code = ''
        self.lm_job = ''
        self.LM_CO_WAIT = 0
        self.LM_DUP_NONE = 0

        self.origTokens = []
        self.availTokens = []
        self.checkouted = False
        self.lock = threading.Lock()
        
        self.checkoutLic()
        
    def checkoutLic(self):
        scl_lc_enable_abt()
        scl_lc_ch_init(self.prodName, self.prodVersion)
        if not scl_lc_new_job(None, None, self.code, self.lm_job):
            print('Initialization failed ...')
            sys.exit(-1)
        print('Checking out a license from the server ...')
        if not scl_lc_checkout(self.lm_job, self.keyStr, self.verStr, 1, self.LM_CO_WAIT, self.code, self.LM_DUP_NONE):
            print('Checkout failed ...')
            sys.exit(-1)
        if self.keyStr == 'NewFeature':
            self.scl_token_handle = scl_lc_init_token(self.keyStr, self.nlic * 10)
            for i in range(self.nlic * 10) :
                token = scl_lc_get_token(self.scl_token_handle, i)
                self.origTokens.append(token)
                self.availTokens = self.origTokens.copy()
        self.checkouted = True
        
    def getFeature(self):
        return self.keyStr

    ## Check the license use token or not
    # @return True:use token, False: not use token
    def useTokens(self):
        if self.origTokens:
            return True
        return False
    
    def getNlic(self):
        return self.nlic

    def isCheckout(self):
        return self.checkouted

    def isAvailableTokens(self):
        with self.lock:
            if self.availTokens:
                return True
            return False
    ## pop a token to use
    #
    # @return token: when has a token, None: when no token
    def popToken(self):
        with self.lock:
            if self.availTokens:
                return self.availTokens.pop()
            return None
    ## push a token back, the token should be in the original token list
    #  and has been popout
    #
    # @param token Token to push back
    # @return True: if success, False: if failure
    def pushToken(self, token):
        with self.lock:
            if token in self.origTokens and not (token in self.availTokens):
                self.availTokens.append(token)
                return True
            return False

if __name__ == '__main__':
    a = LicManager('xa', '2008.09', 'NewFeature', 2)
    # print(id(a))
    for i in range(21):
        print (a.popToken())
