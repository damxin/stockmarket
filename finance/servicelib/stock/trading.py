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


def insertIntoNormalDbFromNotDealDBData(dbCntInfo,pcodeDataUpdateDict):
    '''
    从临时库的交易数据插入到正式库中
    :param dbCntInfo:
    :param pcodeDataUpdateDict: 记录产品今日是否有数据更新
    :return:
    '''
    print("all productcode data insert begin!")
    sourceTable = "histtradedata"
    destTable = "producttradedata"
    sourceDbBase = dbCntInfo.getDBCntInfoByTableName(sourceTable)
    ordercause = "order by trade_date"
    for productCode, updateFlag in pcodeDataUpdateDict.items():
        if updateFlag in "0":
            continue
        destDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=destTable, productcode=productCode)
        realDataSql = sc.PRODUCTHISTTRADEDATATUSHAREPRO_SQL % (sourceTable+productCode)
        while (True):
            sourceRetList = sourceDbBase.execSelectManySql(realDataSql, ordercause)
            if len(sourceRetList) == 0:
                break
            # 数据插入到另外一个库里面
            sourceList = []
            for oneList in sourceRetList:
                sourceList.append(tuple(oneList.values()))
            destDbBase.execInsertManySql(sc.PRODUCTTRADEDATA_INSERTSQL, sourceList)
    print("all productcode data insert success!")


'''
    获取产品的不复权每日交易数据 Product_trade_data
    autoType=qfq-前复权 hfq-后复权 None-不复权
'''


def getAllNoneSubscriptionTradePriceFromTusharePro(dbCntInfo, autoType=None):
    # 获取产品基础信息
    productBasicInfodf = pb.getAllProductBasicInfo(dbCntInfo)
    if productBasicInfodf.empty:
        print("表中无正在上市的数据，提前正常结束!")
        return
    # 获取当日日期
    finanalWorkDate = pb.getTodayDate()
    curHour = time.localtime().tm_hour
    if curHour < 17:
        finanalWorkDate = pb.getYesterday()

    sourceTable = "histtradedata"
    destTable = "producttradedata"

    # 建立连接与tusharepro
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    engine = dbCntInfo.getEngineByTableName(sourceTable)
    productUpdateDictFlag = {}
    for rowIndex in productBasicInfodf.index:
        oneProductTuple = productBasicInfodf.iloc[rowIndex]
        productCode = oneProductTuple["product_code"]  ## 产品代码
        listedDate = oneProductTuple["listed_date"]  ## 上市日期
        # 获取产品的起始日期,产品可能已经存在部分行情
        maxTradeDateSql = sc.PRODUCTMAXTRADEDATE_SQL % productCode
        destDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=destTable,productcode=productCode)
        destRetList = destDbBase.execSelectSmallSql(maxTradeDateSql)
        maxTradeDate = destRetList[0]['maxtradedate']
        print(rowIndex)
        print(productCode+maxTradeDateSql)
        startDate = listedDate
        if maxTradeDate > listedDate:
            startDate = ((int(maxTradeDate / 10000)) + 1) * 10000 + 101
        endDate = ((int(startDate / 10000))+10) * 10000 + 1231
        if int(listedDate / 10000) == int(finanalWorkDate / 10000):
            endDate = finanalWorkDate
        if endDate > finanalWorkDate:
            endDate = finanalWorkDate
        if startDate > finanalWorkDate:
            productUpdateDictFlag[productCode] = "0"
            continue
        print("%s begin to get data from %d to %d ..." % (productCode, startDate, endDate))
        symbolProcuctCode = pb.code_to_symbol(productCode)
        try :
            productUpdateDictFlag[productCode] = "1"
            df = pro.daily(ts_code=symbolProcuctCode, start_date=str(startDate), end_date=str(endDate))
            basicdf = df.reset_index(drop=True)
            realsourcetable = sourceTable+productCode
            basicdf.to_sql(realsourcetable, engine, if_exists="replace", index=False)
        except Exception as e:
            print(productCode+" connect time out!")
            time.sleep(30)
            df = pro.daily(ts_code=symbolProcuctCode, start_date=str(startDate), end_date=str(endDate))
            basicdf = df.reset_index(drop=True)
            realsourcetable = sourceTable + productCode
            basicdf.to_sql(realsourcetable, engine, if_exists="replace", index=False)
        while endDate < finanalWorkDate:
            startDate = ((int(endDate / 10000)) + 1) * 10000 + 101
            endDate = ((int(startDate / 10000)) + 10) * 10000 + 1231
            if startDate > finanalWorkDate:
                break
            if endDate > finanalWorkDate:
                endDate = finanalWorkDate
            print("%s is getting data from %d to %d ..." % (productCode, startDate, endDate))
            time.sleep(0.5)
            try:
                df = pro.daily(ts_code=symbolProcuctCode, start_date=str(startDate), end_date=str(endDate))
                basicdf = df.reset_index(drop=True)
                basicdf.to_sql(realsourcetable, engine, if_exists="append", index=False)
            except Exception as e:
                print(productCode + " connect time out!")
                time.sleep(30)
                df = pro.daily(ts_code=symbolProcuctCode, start_date=str(startDate), end_date=str(endDate))
                basicdf = df.reset_index(drop=True)
                basicdf.to_sql(realsourcetable, engine, if_exists="append", index=False)
        print(productCode + " begin to get data finish ...")

        if rowIndex % 10 == 0:
            time.sleep(3)
        if rowIndex % 80 == 0:
            time.sleep(90)

    print("all productcode finish download data!")

    insertIntoNormalDbFromNotDealDBData(dbCntInfo, productUpdateDictFlag)
    dbCntInfo.closeAllDBConnect()

def getprofitdata(dbCntInfo):
    '''
        数据来源：http://f10.eastmoney.com/BonusFinancing/Index?type=web&code=sh601199
        中财网:http://data.cfi.cn/cfidata.aspx?sortfd=&sortway=&curpage=1&ndk=A0A1934A1939A1957A1966A1983&xztj=&mystock=
        分红产品分红数据获取
    '''
    df = ts.profit_divis()
    basicdf = df.reset_index(drop=False)
    tablename = 'profit_divis'
    engine = dbCntInfo.getEngineByTableName(tablename)
    basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
    print("finish")


if __name__ == "__main__":
    filedata = open(".\stock_basics.txt", 'w+')
    # xmlfile = "E:\\pydevproj\\stockmarket\\finance\\resource\\finance.xml"
    xmlfile = "F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    dbCntInfo = dbcnt.DbCnt(xmlfile)
    # getprofitdata(dbCntInfo)
    # getStockBasicsPro(dbCntInfo)
    # getProductBasicInfo(dbCntInfo)
    # getAllNoneSubscriptionTradePriceFromTusharePro(dbCntInfo)
    pcodeDataUpdateDict = {}
    pcodeDataUpdateDict["000008"] = "1"
    pcodeDataUpdateDict["300100"] = "1"
    print(pcodeDataUpdateDict)
    try :
        insertIntoNormalDbFromNotDealDBData(dbCntInfo,pcodeDataUpdateDict=pcodeDataUpdateDict)
    finally:
        dbCntInfo.closeAllDBConnect()
    filedata.close()

