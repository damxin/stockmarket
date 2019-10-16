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
from finance.util import DictCons as dc
from finance.servicelib.public import public as pb


def getStockBasics(dbCntInfo, filedata):
    df = ts.get_stock_basics()
    basicdf = df.reset_index(drop=False)
    tablename = 'stock_basics'
    engine = dbCntInfo.getEngineByTableName(tablename)
    basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
    print("finish")

def getStockBasicsPro(dbCntInfo):
    '''
    获取上市产品的信息
    :param dbCntInfo:
    :return:
    '''
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    df = pro.stock_basic()
    basicdf = df.reset_index(drop=True)
    tablename = 'stock_basics_tspro'
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
    logicCntNameList = [sourceLogicName, destLogicName]
    dbCntInfo.getDbCnt(logicCntNameList)
    souceDbBase = dbCntInfo.getDbBaseByLogicName(sourceLogicName)
    destDbBase = dbCntInfo.getDbBaseByLogicName(destLogicName)

    while (True):
        sourceRetList = souceDbBase.execSelectManySql(sc.PRODUCTBASICINFO_SQL)
        if len(sourceRetList) == 0:
            break
        # 数据插入到另外一个库里面
        sourceList = []
        for oneList in sourceRetList:
            print(oneList)
            oneList['market_type'] = dc.DICTCONS_CODETOMARKETTYPE[oneList['market_type']]
            sourceList.append(tuple(oneList.values()))
        # print(type(sourceList))
        # print(type(sourceList[0]))
        # print(sourceList)
        destDbBase.execInsertManySql(sc.PRODUCTBASICINFO_INSERTSQL, sourceList)

    souceDbBase.closeDBConnect()
    destDbBase.closeDBConnect()


'''
    获取产品的资产负债表
    product_code 获取指定产品
'''


def getSpecialCompanyBalanceSheet(product_code):
    if len(product_code) == 0:
        return


'''
    获取产品的资产负债表
    product_code 如果为*，则获取所有的产品
                 为具体值，则获取指定产品
'''


def getCompanyBalanceSheet(product_code):
    if product_code in gc.CONST_STR_STAR:
        return


'''
    获取产品的不复权每日交易数据 Product_trade_data
    autoType=qfq-前复权 hfq-后复权 None-不复权
'''


def getAllNoneSubscriptionTradePriceFromTushare(dbCntInfo, autoType=None):
    # 获取产品基础信息
    productBasicInfodf = pb.getAllProductBasicInfo(dbCntInfo)

    # 获取当日日期
    finanalWorkDate = 20191013
    sourceTable = "histtradedata"
    destTable = "producttradedata"
    sourceLogicName = dbCntInfo.getLogicNameListByTableName(sourceTable)
    destLogicName = dbCntInfo.getLogicNameListByTableName(destTable)
    logicCntNameList = [sourceLogicName, destLogicName]
    dbCntInfo.getDbCnt(logicCntNameList)
    sourceDbBase = dbCntInfo.getDbBaseByLogicName(sourceLogicName)
    destDbBase = dbCntInfo.getDbBaseByLogicName(destLogicName)

    nrow = productBasicInfodf.nrow
    for rowIndex in range(0, nrow):
        oneProductTuple = productBasicInfodf.iloc[rowIndex]
        productCode = oneProductTuple["product_code"]  ## 产品代码
        listedDate = oneProductTuple["listed_date"]  ## 上市日期
        # 获取产品的起始日期
        maxTradeDateSql = sc.PRODUCTMAXTRADEDATE_SQL % productCode
        destRetList = destDbBase.execSelectManySql(maxTradeDateSql)
        maxTradeDate = destRetList[0]
        startDate = listedDate
        if maxTradeDate > listedDate:
            startDate = maxTradeDate
        endDate = startDate / 10000 * 10000 + 1231
        if listedDate / 10000 == finanalWorkDate / 10000:
            endDate = finanalWorkDate
        strStartDate = pb.dateSpecailFormat(startDate)
        strEndDate = pb.dateSpecailFormat(endDate)
        df = ts.get_h_data(productCode, start=strStartDate, end=strEndDate, autype=None)
        basicdf = df.reset_index(drop=False)
        # 这里要看下会不会有问题
        engine = dbCntInfo.getEngineByTableName(sourceTable)
        basicdf.to_sql(sourceTable, engine, if_exists="replace", index=False)
        while endDate < finanalWorkDate:
            startDate = (startDate / 10000 + 1) * 10000 + 101
            endDate = (endDate / 10000 + 1) * 10000 + 1231
            if startDate > finanalWorkDate:
                break
            if endDate > finanalWorkDate:
                endDate = finanalWorkDate
            strStartDate = pb.dateSpecailFormat(startDate)
            strEndDate = pb.dateSpecailFormat(endDate)
            df = ts.get_h_data(productCode, start=strStartDate, end=strEndDate, autype=None)
            basicdf = df.reset_index(drop=False)
            basicdf.to_sql(sourceTable, engine, if_exists="append", index=False)
        while (True):
            sourceRetList = sourceDbBase.execSelectManySql(sc.PRODUCTHISTTRADEDATA_SQL)
            if len(sourceRetList) == 0:
                break
            # 数据插入到另外一个库里面
            print(type(sourceRetList))
            print(sourceRetList)
            destDbBase.execInsertManySql(sc.PRODUCTTRADEDATA_INSERTSQL, sourceRetList)

    sourceDbBase.closeDBConnect()
    destDbBase.closeDBConnect()


'''
    获取产品的不复权每日交易数据 Product_trade_data
    autoType=qfq-前复权 hfq-后复权 None-不复权
'''


def getAllNoneSubscriptionTradePriceFromTusharePro(dbCntInfo, autoType=None):
    # 获取产品基础信息
    productBasicInfodf = pb.getAllProductBasicInfo(dbCntInfo)

    # 获取当日日期
    finanalWorkDate = 20191013
    sourceTable = "histtradedata"
    destTable = "producttradedata"
    sourceLogicName = dbCntInfo.getLogicNameListByTableName(sourceTable)
    destLogicName = dbCntInfo.getLogicNameListByTableName(destTable)
    logicCntNameList = [sourceLogicName, destLogicName]
    dbCntInfo.getDbCnt(logicCntNameList)
    sourceDbBase = dbCntInfo.getDbBaseByLogicName(sourceLogicName)
    destDbBase = dbCntInfo.getDbBaseByLogicName(destLogicName)

    # 建立连接与tusharepro
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')

    #    nrow = productBasicInfodf.nrow
    nrow = 1
    ordercause = "order by trade_date"
    for rowIndex in range(0, nrow):
        oneProductTuple = productBasicInfodf.iloc[rowIndex]
        productCode = oneProductTuple["product_code"]  ## 产品代码
        listedDate = oneProductTuple["listed_date"]  ## 上市日期
        # 获取产品的起始日期,产品可能已经存在部分行情
        maxTradeDateSql = sc.PRODUCTMAXTRADEDATE_SQL % destTable
        destRetList = destDbBase.execSelectSmallSql(maxTradeDateSql)
        maxTradeDate = destRetList[0]['maxtradedate']
        startDate = listedDate
        if maxTradeDate > listedDate:
            startDate = maxTradeDate
        endDate = (int(startDate / 10000)) * 10000 + 1231
        if listedDate / 10000 == finanalWorkDate / 10000:
            endDate = finanalWorkDate
        print("%s begin to get data from %d to %d ..." % (productCode, startDate, endDate))
        symbolProcuctCode = pb.code_to_symbol(productCode)
        df = pro.daily(ts_code=symbolProcuctCode, start_date=str(startDate), end_date=str(endDate))
        basicdf = df.reset_index(drop=True)
        engine = dbCntInfo.getEngineByTableName(sourceTable)
        basicdf.to_sql(sourceTable, engine, if_exists="replace", index=False)
        while endDate < finanalWorkDate:
            startDate = (startDate / 10000 + 1) * 10000 + 101
            endDate = ((int(endDate / 10000)) + 1) * 10000 + 1231
            if startDate > finanalWorkDate:
                break
            if endDate > finanalWorkDate:
                endDate = finanalWorkDate
            df = pro.daily(ts_code=symbolProcuctCode, start_date=str(startDate), end_date=str(endDate))
            basicdf = df.reset_index(drop=True)
            basicdf.to_sql(sourceTable, engine, if_exists="append", index=False)
            break
        while (True):
            sourceRetList = sourceDbBase.execSelectManySql(sc.PRODUCTHISTTRADEDATATUSHAREPRO_SQL, ordercause)
            if len(sourceRetList) == 0:
                break
            # 数据插入到另外一个库里面
            sourceList = []
            for oneList in sourceRetList:
                sourceList.append(tuple(oneList.values()))
            destDbBase.execInsertManySql(sc.PRODUCTTRADEDATA_INSERTSQL, sourceList)
            break
        break

    sourceDbBase.closeDBConnect()
    destDbBase.closeDBConnect()

def getprofitdata(dbCntInfo):
    '''
        数据来源：http://f10.eastmoney.com/BonusFinancing/Index?type=web&code=sh601199
        分红产品分红数据获取
    '''
    return


if __name__ == "__main__":
    filedata = open(".\stock_basics.txt", 'w+')
    xmlfile = "E:\\pydevproj\\stockmarket\\finance\\resource\\finance.xml"
    #     xmlfile = "F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    dbCntInfo = dbcnt.DbCnt(xmlfile)
    getStockBasicsPro(dbCntInfo)
    # getProductBasicInfo(dbCntInfo)
    # getAllNoneSubscriptionTradePriceFromTusharePro(dbCntInfo)
    filedata.close()
