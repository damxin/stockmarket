# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

'''
    提供公共的接口
'''

from finance.servicelib.processinit import dbcnt
from finance.util import SqlCons as sc
import pandas as pd

def getAllProductBasicInfo(dbCntInfo):
    tablename = "productbasicinfo"
    tableLogicName = dbCntInfo.getLogicNameListByTableName(tablename)
    logicCntNameList = [tableLogicName]
    dbCntInfo.getDbCnt(logicCntNameList)
    tableDbBase = dbCntInfo.getDbBaseByLogicName(tableLogicName)

    tableRetTuple = tableDbBase.execSelectSmallSql(sc.PRODUCTBASICINFO_SQL)
    if len(tableRetTuple) == 0:
        return
    # 数据插入到另外一个库里面
    

    tableDbBase.closeDBConnect()
    return pd.DataFrame(tableRetTuple)

'''
    20190102格式化为2019-01-02
'''
def dateSpecailFormat(intDateFormat):
    if intDateFormat < 10000000:
        print("date format is exception!", end="")
        print(intDateFormat)
        raise Exception("date format is exception!")
    strDate = ""
    strDate = strDate + intDateFormat/10000 + "-"
    strDate = strDate + intDateFormat/100%100 + "-"
    strDate = strDate + intDateFormat%100
    return strDate

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

    while(True):
        sourceRetList = souceDbBase.execSelectManySql(sc.PRODUCTBASICINFO_SQL)
        if len(sourceRetList) == 0:
            break
        # 数据插入到另外一个库里面
        destDbBase.execInsertManySql(sc.PRODUCTBASICINFO_INSERTSQL,sourceRetList)

    souceDbBase.closeDBConnect()
    destDbBase.closeDBConnect()