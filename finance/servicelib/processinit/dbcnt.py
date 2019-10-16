# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

from finance.dbsql import mysqldatabase
from finance.dbsql import oracledatabase
from sqlalchemy import create_engine
from finance.servicelib.processinit.xmlcfg import XmlCfg
from finance.util import GlobalCons as gc
from finance.util import SqlCons as sc


class DbCnt:
    def __init__(self, xmlfilepath):
        dbCfg = XmlCfg(xmlfilepath)
        dbCfgInfoDicts = dbCfg.getDbInfoFromXmlFile()
        self.dbCfgInfoDicts = dbCfgInfoDicts
        self.dbCntdicts = {}

    def getDbCnt(self, logicCntNameList):
        for logicNameKey, dbCfgInfoValue in self.dbCfgInfoDicts.items():
            print(logicNameKey)
            print(dbCfgInfoValue)
            if logicNameKey not in logicCntNameList:
                continue
            dbType = dbCfgInfoValue[gc.DBTYPEKEY]
            if dbType == gc.MYSQLDB:
                msqldbase = mysqldatabase.MysqlDatabase(dbCfgInfoValue[gc.SERVERKEY], dbCfgInfoValue[gc.PORTKEY],
                                                        dbCfgInfoValue[gc.USERNAMEKEY], dbCfgInfoValue[gc.PASSWORDKEY],
                                                        dbCfgInfoValue[gc.DATABASEKEY])
                msqldbase.createConnection()
                self.dbCntdicts[logicNameKey] = msqldbase
            elif dbType == gc.ORACLEDB:
                oracledbase = oracledatabase.OracleDatabase(dbCfgInfoValue[gc.SERVERKEY], dbCfgInfoValue[gc.PORTKEY],
                                                            dbCfgInfoValue[gc.USERNAMEKEY],
                                                            dbCfgInfoValue[gc.PASSWORDKEY],
                                                            dbCfgInfoValue[gc.DATABASEKEY])
                oracledbase.createConnection()
                self.dbCntdicts[logicNameKey] = oracledbase

    def getLogicNameListByTableName(self, tablename):
        if tablename in sc.TABLEDICT:
            logicname = sc.TABLEDICT[tablename]
            ## 暂时默认都在trade1
            if logicname[:-1] in "trade":
                reallogicname = logicname[:-1]+"1"
            else:
                reallogicname = logicname

            return reallogicname
        else:
            print(tablename + " is not in dict! error!!")
            raise RuntimeError(tablename + " is not in dict! error!!")
        return

    def getEngineByTableName(self, tablename):
        if tablename in sc.TABLEDICT:
            logicname = sc.TABLEDICT[tablename]
            if logicname in self.dbCfgInfoDicts:
                logicvalue = self.dbCfgInfoDicts[logicname]
                if logicvalue[gc.DBTYPEKEY] in gc.MYSQLDB:
                    enginesql = "mysql+pymysql://" + logicvalue[gc.USERNAMEKEY] + ":" + logicvalue[gc.PASSWORDKEY] + \
                                "@" + logicvalue[gc.SERVERKEY] + "/" + logicvalue[gc.DATABASEKEY] + "?charset=utf8"
                    engine = create_engine(enginesql)
                    return engine
                elif logicvalue[gc.DBTYPEKEY] in gc.ORACLEDB:
                    print("oracle is not support engine! error!")
        print(tablename + " is not in tabledict! error!")
        raise RuntimeError(tablename + " is not in tabledict! error!")
        return

    def getDbBaseByLogicName(self, logicName):
        if logicName in self.dbCntdicts:
            dbSqlBase = self.dbCntdicts[logicName]
            return dbSqlBase
        print(logicName + " do not exist in finance.xml! error!")
        raise RuntimeError(logicName + " do not exist in finance.xml! error!")
        return

# if __name__ == '__main__':
#     dbCnt = DbCnt("F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml")
#     dbCnt.getDbCnt()
