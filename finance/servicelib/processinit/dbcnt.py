# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

from finance.dbsql import mysqldatabase
from finance.dbsql import oracledatabase
from finance.servicelib.processinit.xmlcfg import XmlCfg

class DbCnt:
    def __init__(self,xmlfilepath):
        dbCfg = XmlCfg(xmlfilepath)
        dbCfgInfoDicts = dbCfg.getDbInfoFromXmlFile()
        self.dbCfgInfoDicts = dbCfgInfoDicts
        self.dbCntdicts={}

    def getDbCnt(self):
        for logicNameKey,dbCfgInfoValue in self.dbCfgInfoDicts.items():
            print(logicNameKey)
            print(dbCfgInfoValue)
        # mysqldbase = mysqldatabase.MysqlDatabase("127.0.0.1", "3306", "root", "root", "stockmarket")
        # mysqldbase.getConnection()
        # mysqldbase.closeDBConnect()

if __name__ == '__main__':
    dbCnt = DbCnt("F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml")
    dbCnt.getDbCnt()