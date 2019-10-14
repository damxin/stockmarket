# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

import tushare as ts
import time

from finance.dbsql import mysqldatabase
from finance.servicelib.processinit import dbcnt
from finance.util import SqlCons as sc
from finance.util import GlobalCons as gc

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

    while(True):
        sourceRetList = souceDbBase.execSelectManySql(sc.PRODUCTBASICINFO_SQL)
        if len(sourceRetList) == 0:
            break
        # 数据插入到另外一个库里面
        destDbBase.execInsertManySql(sc.PRODUCTBASICINFO_INSERTSQL,sourceRetList)

    souceDbBase.closeDBConnect()
    destDbBase.closeDBConnect()

'''
    获取产品的资产负债表
    product_code 获取指定产品
'''
def getSpecialCompanyBalanceSheet(product_code):
    if len(product_code)=0:
        return

'''
    获取产品的资产负债表
    product_code 如果为*，则获取所有的产品
                 为具体值，则获取指定产品
'''
def getCompanyBalanceSheet(product_code):
    if product_code in gc.CONST_STR_STAR:
    
'''
    获取产品的不复权每日交易数据 Product_trade_data
    autoType=qfq-前复权 hfq-后复权 None-不复权
'''
def getAllNoneSubscriptionTradePrice(dbCntInfo, autoType=None):
    # 获取作日日期
    finanalWorkDate = 20191013
    # 获取产品基础信息
    productBasicInfodf = getAllProductBasicInfo(dbCntInfo)
    
    nrow = productBasicInfodf.nrow
    for rowIndex in range(0,nrow):
        oneProductTuple = productBasicInfodf.iloc[rowIndex]
        productCode = oneProductTuple["product_code"] ## 产品代码
        listedDate = oneProductTuple["listed_date"] ## 上市日期
        # 获取产品的起始日期
        
        startDate = listedDate
        endDate = startDate/10000*10000+1231
        if listedDate/10000 == finanalWorkDate/10000:
            endDate = finanalWorkDate
        strStartDate = dateSpecailFormat(startDate)
        strEndDate = dateSpecailFormat(endDate)
        df = ts.get_h_data(productCode, start=strStartDate, end=strEndDate,autype=None)
        basicdf = df.reset_index(drop=False)
        tablename = "hdata_" + productCode
        engine = dbCntInfo.getEngineByTableName(tablename)
        basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
        if endDate != finanalWorkDate:
            while endDate < finanalWorkDate:
                startDate = (startDate/10000+1)*10000+101
                endDate = (endDate/10000+1)*10000+1231
                if startDate > finanalWorkDate:
                    break
                if endDate > finanalWorkDate:
                    endDate = finanalWorkDate:
                strStartDate = dateSpecailFormat(startDate)
                strEndDate = dateSpecailFormat(endDate)
                df = ts.get_h_data(productCode, start=strStartDate, end=strEndDate,autype=None)
                basicdf = df.reset_index(drop=False)
                basicdf.to_sql(tablename, engine, if_exists="append", index=False)




if __name__ == "__main__":
    filedata = open(".\stock_basics.txt", 'w+')
    xmlfile = "F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    dbCntInfo = dbcnt.DbCnt(xmlfile)
    getStockBasics(dbCntInfo,filedata)
    getProductBasicInfo()
    filedata.close()