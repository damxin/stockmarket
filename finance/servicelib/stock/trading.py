# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

import os
import tushare as ts
import time
import pandas as pd
import logging

from finance.dbsql import mysqldatabase
from finance.servicelib.processinit import dbcnt
from finance.servicelib.processinit import stocklog
from finance.util import SqlCons as sc
from finance.util import GlobalCons as gc
from finance.util import DictCons as dc
from finance.servicelib.public import public as pb


# from finance.util.formula import MA


def getStockBasics(dbCntInfo):
    # pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    # df = pro.stock_basics()
    df = ts.get_stock_basics()
    basicdf = df.reset_index(drop=False)
    tablename = 'stock_basics'
    engine = dbCntInfo.getEngineByTableName(tablename)
    basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
    print("basic finish")


def getDelistStockBasics(dbCntInfo):
    '''
    获取退市的股票 list
    :return:
    '''
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    df = pro.stock_basic(list_status='D', fields='ts_code,symbol,name,area,industry,list_date,delist_date')
    # basicdf = df.reset_index(drop=False)
    # tablename = 'deliststock'
    # engine = dbCntInfo.getEngineByTableName(tablename)
    # basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
    print("delist finish")
    return df


def getProductBasicInfo():
    '''
    productbasicinfo表信息更新
    :param dbCntInfo:
    :return:
    '''

    dbCntInfo = dbcnt.getInitDbCntInfo()
    sourceTable = "stock_basics"
    getStockBasics(dbCntInfo)
    destTable = "productbasicinfo"
    souceDbBase = dbCntInfo.getDBCntInfoByTableName(sourceTable)
    destDbBase = dbCntInfo.getDBCntInfoByTableName(destTable)
    proctBaseInfoDf = pb.getAllProductBasicInfo(dbCntInfo, ipostatus="N", producttype='1')
    productcodelist = proctBaseInfoDf["product_code"].tolist()

    while (True):
        sourceRetList = souceDbBase.execSelectManySql(sc.PRODUCTBASICINFO_SQL, " order by code")
        if len(sourceRetList) == 0:
            break

        curworkday = pb.getlastworkday()
        # 数据插入到另外一个库里面
        newsourceListTuple = []

        for oneList in sourceRetList:
            productcode = oneList["product_code"]
            if productcode not in productcodelist:
                print(oneList)
                oneList['market_type'] = dc.DICTCONS_CODETOMARKETTYPE[oneList['market_type']]
                oneList['symbol_code'] = pb.code_to_symbol(productcode)
                newsourceListTuple.append(tuple(oneList.values()))

        if len(newsourceListTuple) != 0:
            destDbBase.execInsertManySql(sc.PRODUCTBASICINFO_INSERTSQL, newsourceListTuple)

    proctBaseInfoDf = getDelistStockBasics(dbCntInfo)
    proctBaseInfoDf = proctBaseInfoDf.set_index("symbol")
    delistListTuple = []
    for productcode,itemvalue in proctBaseInfoDf.iterrows():
        if productcode in productcodelist:
            # print("%s has delisted!" % productcode)
            # print(itemvalue)
            delistListTuple.append(
                (itemvalue["delist_date"], pb.code_to_symbol(productcode)))
    if len(delistListTuple) != 0:
        # print(delistListTuple)
        destDbBase.execupdatemanysql(sc.PRODUCTBASICINFO_UPDATEDELISTSQL, delistListTuple)

    # souceDbBase.closeDBConnect()
    # destDbBase.closeDBConnect()

def getIndexBasicInfo():
    '''
    获取指数数据的基础信息
    :return:
    '''
    dbCntInfo = dbcnt.getInitDbCntInfo()
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    # df = pro.fund_basic(status = 'L')
    df = pro.fund_daily(trade_date='20200803')
    basicdf = df.reset_index(drop=False)
    tablename = 'indextradedata'
    engine = dbCntInfo.getEngineByTableName(tablename)
    basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
    print(df)


def insertIntoNormalDbFromNotDealDBData(dbCntInfo, startdate, pcodeDataUpdateDict):
    '''
    从临时库的交易数据插入到正式库中
    :param dbCntInfo:
    :param startdate 0：通过产品一只一只获取 非0:是通过日期一起获取
    :param pcodeDataUpdateDict: 记录产品今日是否有数据更新
    :return:
    '''
    print("all symbolcode data insert begin!")
    sourceTable = "histtradedata"
    destTable = "producttradedata"
    sourceDbBase = dbCntInfo.getDBCntInfoByTableName(sourceTable)
    ordercause = "order by trade_date"
    for symbolcode, updateFlag in pcodeDataUpdateDict.items():
        if updateFlag in "0":
            continue
        destDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=destTable, symbolcode=symbolcode)
        if startdate == 0:
            realDataSql = sc.PRODUCTHISTTRADEDATATUSHAREPRO_SQL % (sourceTable + symbolcode)
            while (True):
                sourceRetList = sourceDbBase.execSelectManySql(realDataSql, ordercause)
                if len(sourceRetList) == 0:
                    break
                # 数据插入到另外一个库里面
                sourceList = []
                for oneList in sourceRetList:
                    sourceList.append(tuple(oneList.values()))
                destDbBase.execInsertManySql(sc.PRODUCTTRADEDATA_INSERTSQL, sourceList)
        else:
            realDataSql = sc.PRODUCTHISTTRADEDATATUSHAREPRO_SQL % (sourceTable + str(startdate))

    print("all productcode data insert success!")


def getalltradeproductdate(dbCntInfo) -> pd.DataFrame:
    '''
    获取需要获取交易数据的产品的数据
    :param dbCntInfo:
    :return:
    '''
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

    destTable = "producttradedata"
    productcodelist = []
    startdatelist = []
    enddatelist = []
    for rowIndex in productBasicInfodf.index:
        oneProductTuple = productBasicInfodf.iloc[rowIndex]
        productCode = oneProductTuple["product_code"]  ## 产品代码
        listedDate = oneProductTuple["listed_date"]  ## 上市日期
        # 获取产品的起始日期,产品可能已经存在部分行情
        maxTradeDateSql = sc.PRODUCTMAXTRADEDATE_SQL % productCode
        destDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=destTable, productcode=productCode)
        destRetList = destDbBase.execSelectSmallSql(maxTradeDateSql)
        maxTradeDate = destRetList[0]['maxtradedate']
        print(rowIndex)
        print(productCode + maxTradeDateSql)
        startDate = listedDate
        if maxTradeDate > listedDate:
            startDate = pb.getnextnday(maxTradeDate, 1)
        endDate = ((int(startDate / 10000)) + 10) * 10000 + 1231
        if int(listedDate / 10000) == int(finanalWorkDate / 10000):
            endDate = finanalWorkDate
        if endDate > finanalWorkDate:
            endDate = finanalWorkDate
        if startDate > finanalWorkDate:
            continue
        print("startdate(%d),enddate(%d)" % (startDate, endDate))
        productcodelist.append(productCode)
        startdatelist.append(startDate)
        enddatelist.append(endDate)
    if len(productcodelist) > 0:
        dfdict = {"productcode": productcodelist, "startdate": startdatelist, "enddate": enddatelist}
        df = pd.DataFrame(dfdict)
        df = df.set_index("productcode")
        return df
    return


def getCurProductTradeData(productcode, dbCntInfo, engine):
    '''
    通过单一产品代码获取该产品的所有交易数据
    :param dbCntInfo:
    :param productcode:
    :return:
    '''
    # 获取当日日期
    finanalWorkDate = pb.getTodayDate()
    curHour = time.localtime().tm_hour
    if curHour < 17:
        finanalWorkDate = pb.getYesterday()

    sourceTable = "histtradedata"
    destTable = "producttradedata"

    # 建立连接与tusharepro
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')

    oneProductTuple = pb.getCurProductBasicInfoByProductCode(dbCntInfo, productcode)
    productCode = oneProductTuple["product_code"]  ## 产品代码
    listedDate = oneProductTuple["listed_date"]  ## 上市日期
    # 获取产品的起始日期,产品可能已经存在部分行情
    maxTradeDateSql = sc.PRODUCTMAXTRADEDATE_SQL % productCode
    destDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=destTable, productcode=productCode)
    destRetList = destDbBase.execSelectSmallSql(maxTradeDateSql)
    maxTradeDate = destRetList[0]['maxtradedate']
    print(productCode + maxTradeDateSql)
    startDate = listedDate
    if maxTradeDate > listedDate:
        startDate = pb.getnextnday(maxTradeDate, 1)
    endDate = ((int(startDate / 10000)) + 10) * 10000 + 1231
    if int(listedDate / 10000) == int(finanalWorkDate / 10000):
        endDate = finanalWorkDate
    if endDate > finanalWorkDate:
        endDate = finanalWorkDate
    if startDate > finanalWorkDate:
        return
    print("%s begin to get data from %d to %d ..." % (productCode, startDate, endDate))
    symbolProcuctCode = pb.code_to_symbol(productCode)
    try:
        df = pro.daily(ts_code=symbolProcuctCode, start_date=str(startDate), end_date=str(endDate))
        basicdf = df.reset_index(drop=True)
        realsourcetable = sourceTable + productCode
        basicdf.to_sql(realsourcetable, engine, if_exists="replace", index=False)
        engine.connect().commit()
    except Exception as e:
        print(productCode + " connect time out!")
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
    print(productCode + " get data finish ...")


def getAllNoneSubscriptionTradePriceFromTusharePro(dbCntInfo):
    '''
    获取产品的不复权每日交易数据 Producttradedata
    :param dbCntInfo:
    :return:
    '''
    productdf = getalltradeproductdate(dbCntInfo)
    if productdf is None:
        print("Trade datas are not should be get, because of they are newest!")
        return
    ## 按照startdate进行group by进行数据统计
    countstartdate = productdf["startdate"].groupby(productdf["startdate"]).count()
    countenddate = productdf["enddate"].groupby(productdf["enddate"]).count()
    engine = dbCntInfo.getEngineByTableName("histtradedata")
    for productcode in productdf.index:
        oneproductdate = productdf.loc[productcode]
        startdate = oneproductdate["startdate"]
        enddate = oneproductdate["enddate"]
        onecntstartdate = countstartdate.loc[startdate]
        if onecntstartdate < 100 and startdate < enddate:
            getCurProductTradeData(productcode, dbCntInfo, engine)

    sourceTable = "histtradedata"
    destTable = "producttradedata"
    for productcode in productdf.index:
        oneproductdate = productdf.loc[productcode]
        startdate = oneproductdate["startdate"]
        enddate = oneproductdate["enddate"]
        onecntstartdate = countstartdate.loc[startdate]
        if onecntstartdate < 100 and startdate < enddate:
            selectsql = sc.PRODUCTHISTTRADEDATATUSHAREPRO_SQL % (sourceTable + productcode)
            insertsql = sc.PRODUCTTRADEDATA_INSERTSQL
            print(productcode + " trade data insert begin")
            pb.insertNormalDbByCurProductCode(dbCntInfo, sourceTable, destTable, selectsql, insertsql, productcode)
            print(productcode + " trade data insert finish")

    minstartdate = 20991231
    for indexstartdate in countstartdate.index:
        cntstartdate = countstartdate.loc[indexstartdate]
        if cntstartdate >= 100 and indexstartdate < minstartdate:
            minstartdate = indexstartdate
    maxenddate = 0
    for indexenddate in countenddate.index:
        cntenddate = countenddate.loc[indexenddate]
        if cntenddate >= 100 and indexenddate > maxenddate:
            maxenddate = indexenddate
    tradedate = minstartdate
    # 建立连接与tusharepro
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    while tradedate <= maxenddate:
        print("begin to get all data on %d ..." % tradedate)
        df = pro.daily(trade_date=str(tradedate))
        time.sleep(1)
        basicdf = df.reset_index(drop=True)
        realsourcetable = sourceTable + str(tradedate)
        basicdf.to_sql(realsourcetable, engine, if_exists="replace", index=False)
        tradedate = pb.getnextnday(tradedate, 1)

    insertsql = sc.PRODUCTTRADEDATA_INSERTSQL
    for productcode in productdf.index:
        oneproductdate = productdf.loc[productcode]
        startdate = oneproductdate["startdate"]
        enddate = oneproductdate["enddate"]
        cntstartdate = countstartdate.loc[startdate]
        if cntstartdate < 100:
            continue
        tradedate = minstartdate
        print(productcode + " trade data insert begin from %d to %d" % (startdate, enddate))
        while tradedate <= maxenddate and startdate <= tradedate and tradedate <= enddate:
            selectsql = sc.PRODUCTHISTTRADEDATATUSHAREPRO_SQL % (
                    sourceTable + str(tradedate)) + " where left(a.ts_code,6) = '%s'" % productcode
            pb.insertNormalDbByCurProductCode(dbCntInfo, sourceTable, destTable, selectsql, insertsql, productcode)
            tradedate = pb.getnextnday(tradedate, 1)
        print(productcode + " trade data insert finish")

    dbCntInfo.closeAllDBConnect()


def getProfitData(dbCntInfo):
    '''
        在执行前需要首先用下列语句创建表
        USE stocknotdealmarket;
        DROP TABLE IF EXISTS histprofitdata;
        CREATE TABLE histprofitdata (
          ts_code text DEFAULT NULL,
          end_date text DEFAULT NULL,
          ann_date text DEFAULT NULL,
          div_proc text DEFAULT NULL,
          stk_div double DEFAULT NULL,
          stk_bo_rate double DEFAULT NULL,
          stk_co_rate double DEFAULT NULL,
          cash_div double DEFAULT NULL,
          cash_div_tax double DEFAULT NULL,
          record_date text DEFAULT NULL,
          ex_date text DEFAULT NULL,
          pay_date text DEFAULT NULL,
          div_listdate text DEFAULT NULL,
          imp_ann_date text DEFAULT NULL
        )
        数据来源：http://f10.eastmoney.com/BonusFinancing/Index?type=web&code=sh601199
        中财网:http://data.cfi.cn/cfidata.aspx?sortfd=&sortway=&curpage=1&ndk=A0A1934A1939A1957A1966A1983&xztj=&mystock=
        分红产品分红数据获取
    '''
    # 获取产品基础信息
    productBasicInfodf = pb.getAllProductBasicInfo(dbCntInfo)
    if productBasicInfodf.empty:
        print("表中无正在上市的数据，提前正常结束!")
        return
    # 获取当日日期
    # finanalWorkDate = pb.getTodayDate()

    sourceTable = "histprofitdata"  # 分红数据
    # destTable = "profitschema" # 产品分红方案

    # 建立连接与tusharepro
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    engine = dbCntInfo.getEngineByTableName(sourceTable)
    for rowIndex in productBasicInfodf.index:
        oneProductTuple = productBasicInfodf.iloc[rowIndex]
        productCode = oneProductTuple["product_code"]  ## 产品代码

        print("%d %s begin to get prifit data ..." % (rowIndex, productCode))
        symbolProcuctCode = pb.code_to_symbol(productCode)
        try:
            df = pro.dividend(ts_code=symbolProcuctCode)
            basicdf = df.reset_index(drop=True)
            basicdf.to_sql(sourceTable, engine, if_exists="append", index=False)
        except Exception as e:
            print(productCode + " connect time out!")
            time.sleep(30)
            df = pro.dividend(ts_code=symbolProcuctCode)
            basicdf = df.reset_index(drop=True)
            basicdf.to_sql(sourceTable, engine, if_exists="append", index=False)
        print(productCode + " begin to get data finish ...")
        time.sleep(1)

        if rowIndex % 100 == 0:
            time.sleep(10)
        if rowIndex % 500 == 0:
            time.sleep(30)

    print("all productcode profitschema finish download!")
    dbCntInfo.closeAllDBConnect()


# def getTradeDataFromDataBase(product_code, ma=None, autotype=None):
#     '''
#     获取交易数据准备K线图显示
#     :param product_code:
#     :param autotype:None未复权 qfq前复权 hfq后复权
#     :return: dataframe {trade_date,open,close,low,high, ma均线}
#     '''
#     ma = [30,60,99,120,250] if ma is None else ma
#     dataType = autotype.lower() if autotype is not None else "nfq" # nfq 未复权
#     xmlfile = "F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
#     dbCntInfo = dbcnt.DbCnt(xmlfile)
#     sourceTable = "producttradedata"
#     dbSqlSession = dbCntInfo.getDBCntInfoByTableName(sourceTable,product_code)
#     allDataGetSql = sc.PRODUCTTRADEDATA_GETALLDATA_SQL%product_code
#     tradeDataTupleInList = dbSqlSession.execSelectAllSql(allDataGetSql)
#
#     curBaseInfo = pb.getCurProductBasicInfoByProductCode(dbCntInfo,product_code)
#     productname = curBaseInfo["product_name"]
#     dbCntInfo.closeAllDBConnect()
#     dfdata = pb.listdictTypeChangeToDataFrame(tradeDataTupleInList)
#     if dataType not in "nfq":
#         ts_code = pb.code_to_symbol(product_code)
#         pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
#         fcts = pro.adj_factor(ts_code=ts_code, trade_date="")[['trade_date', 'adj_factor']]
#         adjfactortable = "histadjfactor"
#         engine = dbCntInfo.getEngineByTableName(adjfactortable)
#         fcts.to_sql(adjfactortable, engine, if_exists="replace", index=False)
#         fcts['trade_date'] = fcts['trade_date'].astype(int)
#         if fcts.shape[0] == 0:
#             return None
#
#         dfdata = dfdata.set_index('trade_date', drop=False).merge(fcts.set_index('trade_date'), left_index=True,
#                                                                     right_index=True, how='left')
#         dfdata['adj_factor'] = dfdata['adj_factor'].fillna(method='bfill')
#
#         for col in gc.PRICE_COLS:
#             if dataType == 'hfq':
#                 dfdata[col] = dfdata[col] * dfdata['adj_factor']
#             if dataType == 'qfq':
#                 dfdata[col] = dfdata[col] * dfdata['adj_factor'] / float(fcts['adj_factor'][0])
#             dfdata[col] = dfdata[col].map(gc.FORMAT)
#         for col in gc.PRICE_COLS:
#             dfdata[col] = dfdata[col].astype(float)
#         dfdata = dfdata.drop('adj_factor', axis=1)
#     dfclose = dfdata['close'].sort_index(ascending=False)
#     for a in ma:
#         if isinstance(a, int):
#             dfdata['ma%s'%a] = MA(dfclose, a).map(gc.FORMAT).shift(-(a-1))
#             dfdata['ma%s'%a] = dfdata['ma%s'%a].astype(float)
#
#     # dfname._stat_axis.values.tolist() # 行名称
#     # dfname.columns.values.tolist()    # 列名称
#     return productname,dfdata

def getSuspendProduct(dbCntInfo):
    '''
    获取股票每日停复牌信息
    :param dbCntInfo:
    :return:
    '''

    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    df = pro.suspend(ts_code='600848.SH', suspend_date='', resume_date='', fields='')
    return


def getmaxreportdate(dbCntInfo, destTable) -> dict:
    '''
    获取每个产品最大的reportdate
    :param dbCntInfo:
    :return:
    '''
    # 获取产品基础信息
    productBasicInfodf = pb.getAllProductBasicInfo(dbCntInfo)
    if productBasicInfodf.empty:
        print("表中无正在上市的数据，提前正常结束!")
        return

    maxreportdatedict = {}
    for rowIndex in productBasicInfodf.index:
        oneProductTuple = productBasicInfodf.iloc[rowIndex]
        productCode = oneProductTuple["product_code"]  ## 产品代码

        maxReportDateSql = sc.COMPANYMAXREPORTDATE_SQL % (destTable, productCode)
        destDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=destTable, productcode=productCode)
        destRetList = destDbBase.execSelectSmallSql(maxReportDateSql)
        maxReportDate = destRetList[0]['maxreportdate']
        print(rowIndex)
        print(productCode + maxReportDateSql)
        maxreportdatedict[productCode] = maxReportDate
    if len(maxreportdatedict) == 0:
        raise Exception("getmaxreportdate return value is empty!")
    return maxreportdatedict


def getProductFinanceInfo(dbCntInfo, sourcetable, desctable):
    '''
    获取产品的公司财务基础数据
    :param dbCntInfo:
    :param sourcetable: tusharepro数据填写到该表 histincome      histcastflow      histbalance
    :param desctable: 移植到该正式表             company_income  company_cashflow  company_balance_sheet
    :return:
    '''
    productInfoDf = pb.getAllProductBasicInfo(dbCntInfo)
    if productInfoDf.empty:
        print("表中无正在上市的数据，提前正常结束!")
        return

    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    sourceTable = sourcetable  # 比如"histincome"
    destTable = desctable  # 比如"company_income"

    # 获取每个产品已经获取到的最大reportdate
    productReportDateDict = getmaxreportdate(dbCntInfo, destTable)

    engine = dbCntInfo.getEngineByTableName(sourceTable)
    # 获取tusharepro中的数据
    for rowIndex in productInfoDf.index:
        # if rowIndex >= 0:
        #     continue
        if rowIndex % 200 == 0 and rowIndex != 0:
            time.sleep(60)
        oneProductInfo = productInfoDf.iloc[rowIndex]
        productCode = oneProductInfo["product_code"]
        maxreportdate = productReportDateDict[productCode]
        maxreportdate = maxreportdate + 1
        print("%d %s begin to get %s data from intenert..." % (rowIndex, productCode, destTable))
        symbolProcuctCode = pb.code_to_symbol(productCode)
        df = pd.DataFrame()
        try:
            if destTable in "company_income":
                if maxreportdate == 1:
                    df = pro.income(ts_code=symbolProcuctCode)
                else:
                    df = pro.income(ts_code=symbolProcuctCode, start_date=str(maxreportdate))
            elif destTable in "company_balance_sheet":
                if maxreportdate == 1:
                    df = pro.balancesheet(ts_code=symbolProcuctCode)
                else:
                    df = pro.balancesheet(ts_code=symbolProcuctCode, start_date=str(maxreportdate))
            elif destTable in "company_cashflow":
                if maxreportdate == 1:
                    df = pro.cashflow(ts_code=symbolProcuctCode)
                else:
                    df = pro.cashflow(ts_code=symbolProcuctCode, start_date=str(maxreportdate))
            else:
                raise Exception("destTable is exception!")
        except Exception as e:
            print(symbolProcuctCode + " connect time out!")
            time.sleep(120)
            if destTable in "company_income":
                df = pro.income(ts_code=symbolProcuctCode)
            elif destTable in "company_balance_sheet":
                df = pro.balancesheet(ts_code=symbolProcuctCode)
            elif destTable in "company_cashflow":
                df = pro.cashflow(ts_code=symbolProcuctCode)
            else:
                raise Exception("destTable is exception!")
        # 数据去重
        # 数据相同删除重复的数据保留第一个数据
        dfdup = df.drop_duplicates(subset=["ts_code", "end_date"], keep='first', inplace=False)

        realSourTable = sourceTable + productCode
        basicdf = dfdup.reset_index(drop=True)
        basicdf.to_sql(realSourTable, engine, if_exists="replace", index=False)
        print("%s get data finish!" % (productCode))
        time.sleep(1.5)

    # 获取表中存在的数据。
    for rowIndex in productInfoDf.index:
        oneProductInfo = productInfoDf.iloc[rowIndex]
        productCode = oneProductInfo["product_code"]
        maxreportdate = productReportDateDict[productCode]
        realSourTable = sourceTable + productCode
        print("%d %s begin to insert  table %s data..." % (rowIndex, realSourTable, destTable))
        selectsql = sc.COMPANYFINANCE_SELECTSQL[destTable] % (realSourTable, maxreportdate)
        print(selectsql)
        insertsql = sc.COMPANYFINANCE_INSERTSQL[destTable]
        pb.insertNormalDbByCurProductCode(dbCntInfo, sourceTable, destTable, selectsql, insertsql, productCode)
        print("%s insert table %s finish!" % (realSourTable, destTable))

    return


def tdxProductTradeData2Database(dbCntInfo, symbolCode, absolutePath, productTradeFile):
    '''
    单个产品的通达信数据解析后插入到数据库中
    :param dbCntInfo:
    :param symbolCode:
    :param absolutePath:
    :param productTradeFile:
    :return:
    '''

    import struct
    from finance.util import SqlCons as sqlcons

    filepath = absolutePath + productTradeFile

    # 获取该股票的最大日期
    (maxTradeDate, maxTradeTime) = pb.getMaxTradeTimeFromCurProdCode(dbCntInfo, symbolCode)
    if maxTradeDate == 190000101:
        print("当前产品%s没有在productbaseinfo表中,请添加!" % symbolCode)
    print("线程开始正在处理产品代码为(" + symbolCode + ")的文件filepath:" + filepath + "(" + str(maxTradeDate) + ")")
    logging.info("线程开始处理产品代码为(" + symbolCode + ")的文件filepath:" + filepath + "(" + str(maxTradeDate) + ")")
    sourcetable = "producttradedata"
    tableDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=sourcetable, symbolcode=symbolCode)
    with open(filepath, 'rb') as fname:
        while True:
            stock_date = fname.read(4)
            stock_open = fname.read(4)
            stock_high = fname.read(4)
            stock_low = fname.read(4)
            stock_close = fname.read(4)
            stock_amount = fname.read(4)
            stock_vol = fname.read(4)
            stock_reservation = fname.read(4)

            # date,open,high,low,close,amount,vol,reservation

            if not stock_date:
                break
            stock_date = struct.unpack("l", stock_date)  # 4字节 如20091229

            tradedate = stock_date[0]
            if tradedate <= maxTradeDate:
                continue
            stock_open = struct.unpack("l", stock_open)  # 开盘价*100
            openPrice = stock_open[0] / 100.0
            stock_high = struct.unpack("l", stock_high)  # 最高价*100
            highPrice = stock_high[0] / 100.0
            stock_low = struct.unpack("l", stock_low)  # 最低价*100
            lowPrice = stock_low[0] / 100.0
            stock_close = struct.unpack("l", stock_close)  # 收盘价*100
            closePrice = stock_close[0] / 100.0
            stock_amount = struct.unpack("f", stock_amount)  # 成交额
            productAmount = stock_amount[0]
            stock_vol = struct.unpack("l", stock_vol)  # 成交量
            productVolumn = stock_vol[0]
            # stock_reservation = struct.unpack("l", stock_reservation)  # 保留值
            # print("%d,%f"%(tradedate,openPrice))
            # 数据插入到数据库中
            # product_code, trade_date,open_price,high_price,close_price,low_price,product_volume,product_amount
            execlSql = sqlcons.TDXDATAINSERTDATABASE % (
                symbolCode, tradedate, openPrice, highPrice, closePrice, lowPrice, productVolumn, productAmount)
            excepte = tableDbBase.execNotSelectSql(execlSql)
            if excepte is not None:
                print(excepte)
                print("productVolumn(%f),productAmount(%f)" % (productVolumn, productAmount))
                print("执行异常，程序终止!")
                return excepte
    print("线程处理产品代码为(" + symbolCode + ")的文件处理完毕!")
    logging.info("线程处理产品代码为(" + symbolCode + ")的文件处理完毕!")
    return None


def tdxShLdayToStock(dbCntInfo, dataType="sh", softPath="D:/software/new_haitong", relativePath=None):
    '''
    tdx数据读取到数据库中
    参考网站:https://www.jianshu.com/p/9dd3ef74fe96
    tdx目录结构：https://www.cnblogs.com/ftrako/p/3800687.html
    :param softpath:
    :param dataType:
    :return:
    '''

    import os
    import time
    from finance.util import DictCons as dictcons

    relativePath = "/vipdoc/" + dataType + "/lday/" if relativePath is None else relativePath
    absolutePath = softPath + relativePath

    startTime = time.time()
    listTradeFile = os.listdir(absolutePath)
    futurecount = 0
    for productTradeFile in listTradeFile:
        print("正在处理产品代码为的文件:" + productTradeFile)
        productCode = productTradeFile[2:-4]
        # SELECT subleft3 FROM (SELECT  LEFT(a.`product_code`,3) subleft3,a.product_code FROM producttradedata a GROUP BY a.product_code) a GROUP BY subleft3;
        # 000,001,002,003,300,600,601,603,688
        subleft3 = productCode[:3]
        marketType = ""
        symbolcode = productTradeFile[:-4]
        if subleft3 in dictcons.DICTCONS_CODETOMARKETTYPE:
            marketType = dictcons.DICTCONS_CODETOMARKETTYPE[subleft3]
            print("正在处理产品代码为(" + productCode + ")的markettype:" + str(marketType))
        else:
            # print("正在处理产品代码为(" + productCode + ")的文件,跳过该产品:" + subleft3)
            continue
        # sh000001是上证指数，而000001是平安银行是深圳A股，因此这里要过滤
        if dataType == "sz":
            if (marketType == 2 or marketType == 4 or marketType == 3) is False:
                continue
        else:
            if (marketType == 1 or marketType == 8) is False:
                continue
        print("处理第%d的产品代码%s" % (futurecount, symbolcode))
        retresult = tdxProductTradeData2Database(dbCntInfo, symbolcode, absolutePath, productTradeFile)
        if retresult is not None:
            print("%s deal throw except!" % symbolcode)
            return retresult

    print("当前开始时间： ", time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(startTime)))
    print("当前结束时间： ", time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))

    print("future all finished!")

    return None


def tdxProd30TradeData2Database(dbCntInfo, symbolCode, absolutePath, productTradeFile):
    '''
    参考:http://www.360doc.com/content/17/0523/19/8392_656548117.shtml
    解析通达信5min数据，组装成30min数据写入数据库表prod30tradedata中
    :param dbCntInfo:
    :param symbolCode:
    :param path:
    :return:
    '''
    import struct
    import math
    from finance.util import SqlCons as sqlcons

    filename = absolutePath + productTradeFile
    logging.info("start to deal product(" + symbolCode + ")filepath:" + filename)

    # 获取该股票的最大日期
    (maxTradeDate, maxtradetime) = pb.getMaxTradeTimeFromCurProdCode(dbCntInfo, symbolCode, kType=gc.K_30MIN)
    if maxTradeDate == 190000101:
        logging.info("current product(" + symbolCode + ") is not in productbaseinfo, please add!")
    logging.info("product(" + symbolCode + ") maxtradedate:" + str(maxTradeDate))
    sourcetable = "prod30tradedata"
    tableDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=sourcetable, symbolcode=symbolCode)
    execlSql = sqlcons.CSV30DATAINSERTDB
    with open(filename, 'rb') as fname:
        open30price = 0
        high30price = 0
        low30price = 999999999.00
        close30price = 0
        prod30volumn = 0
        prod30amount = 0
        while True:
            buf = fname.read(4 * 8)
            if len(buf) <= 0:
                break
            datetupe = struct.unpack('Ifffffii', buf)
            mds = datetupe[0] & 0xffff
            dateyear = math.floor(mds / 2048) + 2004
            datemonth = math.floor((mds % 2048) / 100)
            dateday = (mds % 2048) % 100
            tradedate = dateyear * 10000 + datemonth * 100 + dateday
            if tradedate <= maxTradeDate:
                continue

            mins = (datetupe[0] >> 16) & 0xffff
            datehour = math.floor(mins / 60)
            datemin = mins % 60
            tradetime = datehour * 10000 + datemin * 100
            openPrice = datetupe[1]
            highPrice = datetupe[2]
            lowPrice = datetupe[3]
            closePrice = datetupe[4]
            productAmount = datetupe[5] / 100
            productVolumn = datetupe[6] / 100
            # stock_reservation = datetupe[7]
            if datemin == 5 or datemin == 35:
                open30price = openPrice
            if datemin == 0 or datemin == 30:
                close30price = closePrice
            high30price = max(high30price, highPrice)
            low30price = min(low30price, lowPrice)
            prod30volumn = prod30volumn + productVolumn
            prod30amount = prod30amount + productAmount

            if datemin == 0 or datemin == 30:
                # product_code,symbol_code, trade_date,trade_time,open_price,high_price,close_price,low_price,product_volume,product_amount
                # trade30datalist.append((productCode, symbolcode, tradedate, tradetime, open30price, high30price,
                #                         close30price, low30price, prod30volumn, prod30amount))
                execlSql = execlSql + sqlcons.CSV30INSERTVAR % (
                    symbolCode, tradedate, tradetime, open30price, high30price,
                    close30price, low30price, prod30volumn, prod30amount)
                if tradetime == 150000:
                    excepte = tableDbBase.execNotSelectSql(execlSql[:-1])
                    if excepte is not None:
                        print(excepte)
                        print("productVolumn(%f),productAmount(%f)" % (productVolumn, productAmount))
                        print("执行异常，程序终止!")
                        return excepte
                    execlSql = sqlcons.CSV30DATAINSERTDB

                open30price = 0
                high30price = 0
                low30price = 999999999.00
                close30price = 0
                prod30volumn = 0
                prod30amount = 0
    logging.info("deal product(" + symbolCode + ")filepath:" + filename + "finish")
    return None


def tdxSh30minToStock(dbCntInfo, dataType='sz', softPath='D:/software/new_haitong'):
    '''
    tdx数据读取到数据库中
    参考网站:https://www.jianshu.com/p/9dd3ef74fe96
    tdx目录结构：https://www.cnblogs.com/ftrako/p/3800687.html
    :param softpath:
    :param dataType:
    :return:
    '''

    import os
    import time
    from finance.util import DictCons as dictcons

    relativePath = "/vipdoc/" + dataType + "/fzline/"
    absolutePath = softPath + relativePath

    startTime = time.time()
    listTradeFile = os.listdir(absolutePath)

    for productTradeFile in listTradeFile:
        productCode = productTradeFile[2:-4]
        symbolCode = productTradeFile[:-4]
        # SELECT subleft3 FROM (SELECT  LEFT(a.`product_code`,3) subleft3,a.product_code FROM producttradedata a GROUP BY a.product_code) a GROUP BY subleft3;
        # 000,001,002,003,300,600,601,603,688
        subleft3 = productCode[:3]
        marketType = ""
        if subleft3 in dictcons.DICTCONS_CODETOMARKETTYPE:
            marketType = dictcons.DICTCONS_CODETOMARKETTYPE[subleft3]
            # print("正在处理产品代码为(" + productCode + ")的markettype:" + str(marketType))
        else:
            # print("正在处理产品代码为(" + productCode + ")的文件,跳过该产品:" + subleft3)
            continue
        # sh000001是上证指数，而000001是平安银行是深圳A股，因此这里要过滤
        if dataType == "sz":
            if (marketType == 2 or marketType == 4 or marketType == 3) is False:
                continue
        else:
            if (marketType == 1 or marketType == 8) is False:
                continue

        # print("处理第%d的产品代码%s" % (futurecount, productCode))
        retresult = tdxProd30TradeData2Database(dbCntInfo, symbolCode, absolutePath, productTradeFile)
        if retresult is not None:
            print("%s deal throw except!" % symbolCode)
            return retresult

    print("当前开始时间： ", time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(startTime)))
    print("当前结束时间： ", time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time())))
    logging.info("future all finished!")
    print("future all finished!")

    return None


def get30tradedata():
    '''
    从get_hist_data中获取30min的数据然后保存到csv中，代码是以下这块，
    然后从csv中读取写入到数据库中
    import os
    import time
    df = ts.get_stock_basics()
    codelist = list(df.index)
    filename = 'E:\\pydevproj\\stockproj\\stockmarket\\finance\\test'
    for oneindex in range(len(codelist)):
        print(codelist[oneindex]+ " begin")
        df = ts.get_hist_data(codelist[oneindex], ktype='30')
        if df is None:
            continue
        realfilename = filename + "\\"+codelist[oneindex]+".csv"
        if os.path.exists(realfilename):
            df.to_csv(realfilename, mode='a', header=None)
        else:
            df.to_csv(realfilename)
        print(codelist[oneindex]+ " end")
        time.sleep(1)
    :return:
    '''
    import os

    import tushare as ts
    import logging
    import csv

    from finance.servicelib.processinit import dbcnt
    from finance.servicelib.processinit import stocklog
    from finance.util import SqlCons as sqlcons
    from finance.servicelib.public import public as pb

    stocklog.initLogging()
    dbCntInfo = dbcnt.createDbConnect(dbpool=False)
    df = ts.get_stock_basics()
    codelist = list(df.index)
    filename = 'G:\\nfx\\stockproj\\stockmarket\\finance\\resource\\trade30'
    for oneindex in range(len(codelist)):
        print(codelist[oneindex] + " begin")
        productCode = codelist[oneindex]
        realfilename = filename + "\\" + productCode + ".csv"
        if os.path.exists(realfilename) is not True:
            logging.info("product(%s) there is no file!" % productCode)
            continue
        logging.info("file(%s) begin to read!" % realfilename)
        sourcetable = "prod30tradedata"
        tableDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=sourcetable, productcode=productCode)
        firstline = 0
        execlSql = sqlcons.CSV30DATAINSERTDB
        with open(realfilename, 'r') as fname:
            reader = csv.reader(fname)
            print(reader)
            for row in reader:
                if firstline == 0:
                    firstline = firstline + 1
                    continue
                # print(row)
                # print(type(row[0]))
                tradedate = int(row[0][:4] + row[0][5:7] + row[0][8:10])
                tradetime = int(row[0][11:13] + row[0][14:16] + row[0][17:19])
                openPrice = float(row[1])
                highPrice = float(row[2])
                closePrice = float(row[3])
                lowPrice = float(row[4])
                productVolumn = float(row[5])
                productAmount = 0.0
                print(tradedate)
                print(tradetime)
                # prod30tradedata(product_code, symbol_code, trade_date, trade_time, open_price, high_price,
                #                 close_price, low_price, product_volume, product_amount)
                symbol_code = pb.code_to_symbol(productCode)
                # print(openPrice)
                # print(highPrice)
                # print(closePrice)
                # print(lowPrice)
                # print(productVolumn)
                # print(symbol_code)
                execlSql = execlSql + sqlcons.CSV30INSERTVAR % (
                    productCode, symbol_code, tradedate, tradetime, openPrice, highPrice, closePrice, lowPrice,
                    productVolumn, productAmount)
                firstline = firstline + 1
                if firstline == 100:
                    excepte = tableDbBase.execNotSelectSql(execlSql[:-1])
                    if excepte is not None:
                        print(excepte)
                        print("执行异常，程序终止!")
                        break
                    execlSql = sqlcons.CSV30DATAINSERTDB
                    firstline = 1
            if len(execlSql) > len(sqlcons.CSV30DATAINSERTDB):
                excepte = tableDbBase.execNotSelectSql(execlSql[:-1])
                if excepte is not None:
                    print(excepte)
                    print("执行异常，程序终止!")
                    break

        logging.info("file(%s) read end!" % realfilename)
    dbCntInfo.closeAllDBConnect()


def dailyDataTdxInsertDb():
    '''
    日线数据从通达信填写到数据库中
    :return:
    '''
    # stocklog.initLogging()
    path = 'D:/software/new_haitong'
    # xmlfile = "G:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    # dbCntInfo = dbcnt.DbCnt(xmlfile, dbpool=False)
    dbCntInfo = dbcnt.getInitDbCntInfo()
    # 5min可以完成
    resultexpt = tdxShLdayToStock(dbCntInfo, "sz", path)
    if resultexpt is None:
        tdxShLdayToStock(dbCntInfo, "sh", path)
    # dbCntInfo.closeAllDBConnect()


def daily30DataTdxInsertDb():
    '''
    30min数据从通达信填写到数据库中
    :return:
    '''
    # 5min可以完成
    # resultexpt = tdxSh30minToStock(dbCntInfo, "sz", path)
    # if resultexpt is None:
    #     tdxSh30minToStock(dbCntInfo, "sh", path)

    path = 'D:/software/new_haitong'
    # xmlfile = "G:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    dbCntInfo = dbcnt.getInitDbCntInfo()
    # 5min可以完成
    resultexpt = tdxSh30minToStock(dbCntInfo, "sz", path)
    if resultexpt is None:
        tdxSh30minToStock(dbCntInfo, "sh", path)
    # dbCntInfo.closeAllDBConnect()


if __name__ == "__main__":
    stocklog.initLogging()
    dbCntInfo = dbcnt.createDbConnect(dbpool=False)
    # import os
    # getProductBasicInfo()
    # dailyDataTdxInsertDb()
    # # # os.sleep(2)
    # daily30DataTdxInsertDb()
    # 获取指数产品
    getIndexBasicInfo()
    # 获取场内基金ETF

    dbCntInfo.closeAllDBConnect()

    # filedata = open(".\stock_basics.txt", 'w+')
    # xmlfile = "E:\\pydevproj\\stockmarket\\finance\\resource\\finance.xml"
    # xmlfile = "F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    # dbCntInfo = dbcnt.DbCnt(xmlfile)
    # getprofitdata(dbCntInfo)
    # getStockBasicsPro(dbCntInfo)
    # getProductBasicInfo(dbCntInfo)
    # getAllNoneSubscriptionTradePriceFromTusharePro(dbCntInfo)
    # getProductFinanceInfo(dbCntInfo, "histincome", "company_income")
    # getProductFinanceInfo(dbCntInfo, "histcastflow", "company_cashflow")
    # getProductFinanceInfo(dbCntInfo, "histbalance", "company_balance_sheet")
    # pcodeDataUpdateDict = {}
    # pcodeDataUpdateDict["000008"] = "1"
    # pcodeDataUpdateDict["300100"] = "1"
    # print(pcodeDataUpdateDict)
    # try :
    #     insertIntoNormalDbFromNotDealDBData(dbCntInfo,pcodeDataUpdateDict=pcodeDataUpdateDict)
    # finally:
    #     dbCntInfo.closeAllDBConnect()
    # getProfitData(dbCntInfo)
    # getAllProductAdjFactorFromTusharePro(dbCntInfo)
    # # getTradeDataFromDataBase("600763",ma=None,autotype="qfq")
    # df = getalltradeproductdate(dbCntInfo)
    #
    # if df is not None:
    #     print(df)
    #     print(df.max())
    #     print(df.min())
    #     print(df.index)
    #     countstartdate = df["startdate"].groupby(df["startdate"]).count()
    #
    #     print(countstartdate)
    #     print(type(countstartdate))
    #     print(countstartdate.index)
    #     alldatadf = pd.merge(df,countstartdate,how="inner",on="startdate")
    #     print(alldatadf.iloc[:3])
    # productCode = "002143"
    # sourceTable = "histtradedata"
    # destTable = "producttradedata"
    # selectsql = sc.PRODUCTHISTTRADEDATATUSHAREPRO_SQL % (sourceTable + productCode)
    # insertsql = sc.PRODUCTTRADEDATA_INSERTSQL
    # insertNormalDbByCurProductCode(productCode, dbCntInfo, sourceTable, destTable, selectsql, insertsql)
    # dbCntInfo.closeAllDBConnect()
    # filedata.close()
