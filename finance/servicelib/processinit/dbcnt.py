# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

from finance.dbsql import mysqldatabase
from finance.dbsql import oracledatabase
from finance.dbsql import dbpool
from sqlalchemy import create_engine
from finance.servicelib.processinit.xmlcfg import XmlCfg
from finance.util import GlobalCons as gc
from finance.util import SqlCons as sc

gDbCntFlag = False
gdbCntInfo = None

def createDbConnect(dbpool=False):
    '''

    :param xmlfile: xml文件所在位置,G:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml
    :param dbpool: 数据库池
    :return:
    '''
    import os

    global gDbCntFlag
    global gdbCntInfo
    pwdpath = os.getcwd()
    financePos = pwdpath.find("finance")
    xmlfile = pwdpath[:financePos] + "finance\\resource\\finance.xml"
    if gDbCntFlag is not True:
        gdbCntInfo = DbCnt(xmlfile, dbpool)
        gDbCntFlag = True
    return gdbCntInfo

def getDBCntInfoByTableName(tableName, symbolCode = None,tradeDate = None):
    global gDbCntFlag
    global gdbCntInfo
    if gDbCntFlag is not True:
        print("database connect does not create,please call function createDbConnect first!")
        return None
    connectDb = gdbCntInfo.getDBCntInfoByTableName(tableName, symbolCode, tradeDate)
    return connectDb

class DbCnt:
    dbthredpool = False

    def __init__(self, xmlfilepath):
        '''
        完成xml文件解析，同时创建所有的数据库连接,单的
        :param xmlfilepath:
        '''
        DbCnt.dbthredpool = False
        dbCfg = XmlCfg(xmlfilepath)
        dbCfgInfoDicts = dbCfg.getDbInfoFromXmlFile()
        self.dbCfgInfoDicts = dbCfgInfoDicts
        self.dbCntdicts = {}
        self.getDbCnt()
        dbcntinfo = self.getDbBaseByLogicName(gc.DBBASELOGICNAME)
        self.dataBaseRule = dbcntinfo.execSelectManySql(sc.DATABASERULE_SQL)
        print(self.dataBaseRule)

    def __init__(self, xmlfilepath, dbpool):
        '''
        完成xml文件解析，同时创建所有的数据库连接池，暂时只支持mysql
        :param xmlfilepath:
        '''
        DbCnt.dbthredpool = dbpool
        dbCfg = XmlCfg(xmlfilepath)
        dbCfgInfoDicts = dbCfg.getDbInfoFromXmlFile()
        self.dbCfgInfoDicts = dbCfgInfoDicts
        self.dbCntdicts = {}
        self.getDbCnt(dbpool)
        dbcntinfo = self.getDbBaseByLogicName(gc.DBBASELOGICNAME)
        self.dataBaseRule = dbcntinfo.execSelectManySql(sc.DATABASERULE_SQL)
        print(self.dataBaseRule)

    def getDbCnt(self, dbispool=False):
        for logicNameKey, dbCfgInfoValue in self.dbCfgInfoDicts.items():
            print(logicNameKey)
            print(dbCfgInfoValue)
            dbType = dbCfgInfoValue[gc.DBTYPEKEY]
            if dbType == gc.MYSQLDB:
                if dbispool is False:
                    msqldbase = mysqldatabase.MysqlDatabase(dbCfgInfoValue[gc.SERVERKEY], dbCfgInfoValue[gc.PORTKEY],
                                                            dbCfgInfoValue[gc.USERNAMEKEY],
                                                            dbCfgInfoValue[gc.PASSWORDKEY],
                                                            dbCfgInfoValue[gc.DATABASEKEY])
                    retsult = msqldbase.createConnection()
                    if retsult == 0:
                        self.dbCntdicts[logicNameKey] = msqldbase
                    else:
                        print("createConnect failed! error!")
                else:
                    msqldbase = dbpool.DbPool(dbCfgInfoValue[gc.SERVERKEY], dbCfgInfoValue[gc.PORTKEY],
                                              dbCfgInfoValue[gc.USERNAMEKEY], dbCfgInfoValue[gc.PASSWORDKEY],
                                              dbCfgInfoValue[gc.DATABASEKEY])
                    retsult = msqldbase.createConnection()
                    if retsult == 0:
                        self.dbCntdicts[logicNameKey] = msqldbase
                    else:
                        print("createConnect failed! error!")
            elif dbType == gc.ORACLEDB:
                oracledbase = oracledatabase.OracleDatabase(dbCfgInfoValue[gc.SERVERKEY], dbCfgInfoValue[gc.PORTKEY],
                                                            dbCfgInfoValue[gc.USERNAMEKEY],
                                                            dbCfgInfoValue[gc.PASSWORDKEY],
                                                            dbCfgInfoValue[gc.DATABASEKEY])
                retsult = oracledbase.createConnection()
                if retsult == 0:
                    self.dbCntdicts[logicNameKey] = oracledbase
                else:
                    print("createConnect failed! error!")

    def getTradeLogicNameByProductCodeAndTradeDate(self, symbolcode, tradedate):
        '''
        返回分库表的逻辑名称
        :param symbolcode:
        :return:
        '''
        if symbolcode is None:
            raise RuntimeError("symbolcode is None! error!!")
        realTradeDate = 0 if tradedate is None else tradedate
        tradeLogicName = ""
        for listIndex in range(len(self.dataBaseRule)):
            oneBaseRuleTuple = self.dataBaseRule[listIndex]
            minProductCode = oneBaseRuleTuple["minproductcode"]
            maxProductCode = oneBaseRuleTuple["maxproductcode"]
            minTradeDate = oneBaseRuleTuple["mintradedate"]
            maxTradeDate = oneBaseRuleTuple["maxtradedate"]
            if minProductCode <= symbolcode <= maxProductCode and minTradeDate <= realTradeDate <= maxTradeDate:
                tradeLogicName = oneBaseRuleTuple["logicname"]
                break
        if len(tradeLogicName) < 1:
            print("%d 's %s do not get trade logic name! error!" % (realTradeDate, symbolcode))
            raise RuntimeError("trade logic name do not get! error!!")
        return tradeLogicName

    def getDBCntInfoByTableName(self, tablename, symbolcode=None, tradedate=None):
        '''

        :param tablename: 表名
        :param productcode: 产品代码
        :param tradedate: 交易日期
        :return:对应的数据库连接信息
        '''
        if tablename in sc.TABLEDICT:
            logicname = sc.TABLEDICT[tablename]
            if logicname in "trade":
                reallogicname = self.getTradeLogicNameByProductCodeAndTradeDate(symbolcode, tradedate)
            else:
                reallogicname = logicname
            dbSqlBase = self.getDbBaseByLogicName(reallogicname)
            return dbSqlBase
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

    def closeAllDBConnect(self):
        '''
        关闭所有的数据库连接
        :return:
        '''
        for dbCntinfo in self.dbCntdicts.values():
            dbCntinfo.closeDBConnect()

# if __name__ == '__main__':
#     dbCnt = DbCnt("F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml")
#     dbCnt.getDbCnt()
