# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

import tushare as ts

from finance.dbsql import mysqldatabase
from finance.servicelib.processinit import dbcnt
from finance.util import SqlCons as sc

def getStockBasics(dbCntInfo,filedata):
    df = ts.get_stock_basics()
    basicdf = df.reset_index(drop=False)
    tablename = 'stock_basics'
    engine = dbCntInfo.getEngineByTableName(tablename)
    basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
    print("finish")
'''
    数据插入到表productbasicinfo中
'''
def getProductBasicInfo(dbCntInfo):
    sourceTable = "stock_basics"
    destTable = "productbasicinfo"
    
    sourceLogicName = dbCntInfo.getLogicNameListByTableName(sourceTable)
    destLogicName = dbCntInfo.getLogicNameListByTableName(destTable)
    logicCntNameList = [sourceLogicName,destLogicName]
    dbCntInfo.getDbCnt(logicCntNameList)    
    souceDbBase = dbCntInfo.getDbBaseByLogicName(sourceLogicName)
    destDbBase = dbCntInfo.getDbBaseByLogicName(destLogicName)

    while(true):
        sourceRetList = souceDbBase.execSelectManySql(sc.PRODUCTBASICINFO_SQL)
        if len(sourceRet) == 0:
            break
        // 数据插入到另外一个库里面
        destDbBase.execInsertManySql(sc.PRODUCTBASICINFO_INSERTSQL,sourceRetList)

    souceDbBase.closeDBConnect()
    destDbBase.closeDBConnect()

if __name__ == "__main__":
    filedata = open(".\stock_basics.txt", 'w+')
    xmlfile = "F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    dbCntInfo = dbcnt.DbCnt(xmlfile)
    getStockBasics(dbCntInfo,filedata)
    getProductBasicInfo()
    filedata.close()