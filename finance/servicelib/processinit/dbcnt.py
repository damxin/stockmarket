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
        '''
        完成xml文件解析，同时创建所有的数据库连接池
        :param xmlfilepath:
        '''
        dbCfg = XmlCfg(xmlfilepath)
        dbCfgInfoDicts = dbCfg.getDbInfoFromXmlFile()
        self.dbCfgInfoDicts = dbCfgInfoDicts
        self.dbCntdicts = {}
        self.getDbCnt()
        dbcntinfo = self.getDbBaseByLogicName(gc.DBBASELOGICNAME)
        self.dataBaseRule = dbcntinfo.execSelectManySql(sc.DATABASERULE_SQL)
        print(self.dataBaseRule)

    def getDbCnt(self):
        for logicNameKey, dbCfgInfoValue in self.dbCfgInfoDicts.items():
            print(logicNameKey)
            print(dbCfgInfoValue)
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

    def getTradeLogicNameByProductCodeAndTradeDate(self,productcode,tradedate):
        '''
        返回分库表的逻辑名称
        :param productcode:
        :return:
        '''
        if productcode is None:
            raise RuntimeError("productcode is None! error!!")
        realTradeDate = 0 if tradedate is None else tradedate
        tradeLogicName = ""
        for listIndex in range(len(self.dataBaseRule)):
            oneBaseRuleTuple = self.dataBaseRule[listIndex]
            minProductCode = oneBaseRuleTuple["minproductcode"]
            maxProductCode = oneBaseRuleTuple["maxproductcode"]
            minTradeDate = oneBaseRuleTuple["mintradedate"]
            maxTradeDate = oneBaseRuleTuple["maxtradedate"]
            if minProductCode <= productcode <= maxProductCode and minTradeDate <= realTradeDate <= maxTradeDate:
                tradeLogicName = oneBaseRuleTuple["logicname"]
                break
        if len(tradeLogicName) < 1:
            print("%d 's %s do not get trade logic name! error!"%(realTradeDate,productcode))
            raise RuntimeError("trade logic name do not get! error!!")
        return tradeLogicName

    def getDBCntInfoByTableName(self, tablename, productcode=None, tradedate=None):
        '''

        :param tablename: 表名
        :param productcode: 产品代码
        :param tradedate: 交易日期
        :return:
        '''
        if tablename in sc.TABLEDICT:
            logicname = sc.TABLEDICT[tablename]
            if logicname in "trade":
                reallogicname = self.getTradeLogicNameByProductCodeAndTradeDate(productcode,tradedate)
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
