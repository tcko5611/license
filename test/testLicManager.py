#! /usr/bin/env python3

import os
import threading
from SclApis.LmServer import LmServer
from CustomFault.LicManager import LicManager 

def runLmServer() :
    LmServer()

if __name__ == '__main__' :
    os.environ['LM_SERVER'] = 'tcko-PC@50008'
    threading.Thread(target = runLmServer).start()
    lic = LicManager('DVP', 2)
    print(lic.isCheckout())
    lic = LicManager('Nanosim', 2)
    print(lic.isCheckout())

    lic = LicManager('NewFeature', 2)
    print(lic.isCheckout())
