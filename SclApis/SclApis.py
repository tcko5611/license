#! /depot/Python-3.5.2/bin/python
import os
import threading
import socket

## @package scl_api
# Documentation for this module.
#
# scl api's module

import socket
import threading

## This API enables anti-binary tampering functionality
#
def scl_lc_enable_abt():
    pass

## This API initiates functionalities required for enabling license robustness.
# @param prod_name The product name.
# @param prod_version The SRM version of the the product
# @return True : Success, False : Failure.
def scl_lc_ch_init(prod_name, prod_version):
    # print('product : {0}, version : {1}'.format(prod_name, prod_version))
    return True

## This API initializes SCL and creates a new job handle.
# @param job Must be none
# @param vendorName Must be None
# @param code VENDORCODE structure
# @param newjob New job handle
# @return True : Success, False : failure
def scl_lc_new_job(job, vendorName, code, newjob):
    return True

## This API checks out one or more licenses for the specified feature.
# @param job job handle created by scl_lc_new_job
# @param feature The feature name to be checked out.
# @param version Vesrion
# @param nlic The number of license.
# @param flag Checkout flag.
# @param code VENDORECODE 
# @param dupflag dup group flag
# @return True : Success, False : failure
def scl_lc_checkout(job, feature, version, nlic, flag, code, dupflag ):
    a = os.environ.get('LM_SERVER')
    if a != None:
        hostPort = a.split('@')
        host = hostPort[0]
        port = int( hostPort[1])
    else :
        print('LM_SERVER(example fsei317@50008) not setting')
        return False
    if feature == 'nanosim/interal_use' :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            data = 'Nanosim'
            s.sendall(data.encode())
            data = s.recv(1024)
            ret = data.decode()
            if ret == 'SUCCESS' :
                return True
        return False
    elif feature == 'CustomSim_Beta' :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            data = 'DVP'
            s.sendall(data.encode())
            data = s.recv(1024)
            ret = data.decode()
            if ret == 'SUCCESS' :
                return True
        return False
    elif feature == 'NewFeature' :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            data = 'NewFeature@' + str(nlic)
            s.sendall(data.encode())
            data = s.recv(1024)
            ret = data.decode()
            if ret == 'SUCCESS' :
                return True
    return False

## This API checks in (releases) the licenses for the specified feature.
# @param job job handle
# @param feature feature name
# @param keep_connect recommend 0
# @return always True
def scl_lc_checkin(job, feature, keep_connect) :
    return True

## This API frees the memory associated with a job handle.
# @param job handle
def scl_lc_free_job(job) :
    return True

## This API will generate the required number of token.   
# @param feature feature name
# @num nimber of tokens to generate
# @return scl token handle or None
def scl_lc_init_token(feature, num) :
    a = os.environ.get('LM_SERVER')
    if a != None:
        hostPort = a.split('@')
        host = hostPort[0]
        port = int( hostPort[1])
    else :
        print('LM_SERVER(example fsei317@50008) not setting')
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        data = 'inittoken@' + str(num)
        s.sendall(data.encode())
        data = s.recv(1024)
        ret = data.decode()
        if ret == 'SUCCESS' :
            return True
        else :
            return False
    return False

## The API is used to retrieve the tokens created by the scl_lc_init_token API.
# @param scl_lc_get_token scl token handle
# @param i index of token
# @param token retrieved token value
# @return : None : failure, token : valid token
def scl_lc_get_token(scl_token_hanle, i):
    a = os.environ.get('LM_SERVER')
    if a != None:
        hostPort = a.split('@')
        host = hostPort[0]
        port = int( hostPort[1])
    else :
        print('LM_SERVER(example fsei317@50008) not setting')
        return None
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

## The API will destroy all the token associated with the handle scl_th
# @param scl_lc_get_token scl token handle
def scl_lc_destroy_token(scl_token_handle):
    #print('destroy token')
    pass

## This API is to be used by the slave.
# @param token token to be validated.
# @return True : success, False : failure.
def scl_lc_validate_token(token):
    a = os.environ.get('LM_SERVER')
    if a != None:
        hostPort = a.split('@')
        host = hostPort[0]
        port = int( hostPort[1])
    else:
        print('LM_SERVER(example fsei317@50008) not setting')
        return False
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
    # import pdb
    # pdb.set_trace()
    #os.environ['LM_SERVER'] = 'fsei317@50008'
    #from LmServer import LmServer
    #t = threading.Thread(target = runLmServer)
    #t.start()

    print(scl_lc_checkout('job', 'SomeKey', '2008/09', 1, 0, 0, 0))
    print(scl_lc_checkout('job', 'CustomSim_Beta', '2008/09', 2, 0, 0, 0))
    print(scl_lc_checkout('job', 'nanosim/interal_use', '2008/09', 2, 0, 0, 0))

    print(scl_lc_checkout('job', 'NewFeature', '2008/09', 2, 0, 0, 0))
    print(scl_lc_init_token('NewFeature', 20))
    for i in range(20):
        print(scl_lc_get_token('job', i))
    print('test addtional token')
    print(scl_lc_get_token('job', 21))
    token = scl_lc_get_token('job', 19)
    print(token)
    if token:
        print(scl_lc_validate_token(token))
    else:
        print('can not get token')
        
        

