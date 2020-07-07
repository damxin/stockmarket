# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''
import os
import logging

# logging.debug("This is a debug log.")
# logging.info("This is a info log.")
# logging.warning("This is a warning log.")
# logging.error("This is a error log.")
# logging.critical("This is a critical log.")

def initLogging(logicname=None):
    '''
    日志初始化
    :return:
    '''
    logicname = "" if logicname is None else logicname
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    # DATE_FORMAT = "%Y-%m-%d,%H:%M:%S"
    pwdpath = os.getcwd()
    financePos = pwdpath.find("finance")
    logpath = pwdpath[:financePos]+"finance\log\stock"+logicname+".log"
    if os.path.exists(logpath):
        os.remove(logpath)
    logging.basicConfig(filename=logpath, level=logging.DEBUG, format=LOG_FORMAT)

if __name__ == "__main__":
    initLogging()
    logging.debug("hello world")
    # pwdpath = os.getcwd()
    # print(pwdpath)
    # financePos = pwdpath.find("finance")
    # print(financePos)
    # print(pwdpath[:financePos]+"finance\log")