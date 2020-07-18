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

'''
    获取交易日历
    exchange_code: str  交易所代码
'''
def getTradeCalendar(dbCntInfo, exchange_code=None):
    print("trade data begin to get...!")
    # 建立连接与tusharepro
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    df = pro.trade_cal(exchange=exchange_code)
    basicdf = df.reset_index(drop=False)
    tablename = 'trade_cal'
    engine = dbCntInfo.getEngineByTableName(tablename)
    basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
    print("trade data finish")


def getaddtradecalendar(dbCntInfo, exchange_code=None):
    '''
    交易日获取，默认获取上交所工作日数据
    :param dbCntInfo: 
    :param exchange_code: SSE上交所，SZE深交所
    :return: 
    '''
    print("trade work day begin to get...")
    exchangecode = exchange_code if exchange_code is not None else "SSE"
    getTradeCalendar(dbCntInfo,exchange_code=exchangecode)
    sourcetable = "trade_cal"
    desttable = "openday"
    # setp1 获取openday中的最大日期和exchangecode
    destDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=desttable)
    selectsql = sc.WORKDAY_MAXDATESQL
    sourceRetDictList = destDbBase.execSelectSmallSql(selectsql)
    if len(sourceRetDictList) == 0:
        print("there is no datas in opneday!")
        onedict = {"maxtradedate":0,"exchangecode":exchangecode}
        sourceRetDictList = [onedict]
    for exchangeinfo in sourceRetDictList:
        maxtradedate = exchangeinfo["maxtradedate"]
        exchangecotmp = exchangeinfo["exchangecode"]
        print("%s start to get workdate from %d"%(exchangecotmp,maxtradedate))
        selectsql = sc.WORKDAY_SQL%(maxtradedate,exchangecotmp)
        insertsql= sc.WORKDAY_INSERTSQL
        pb.insertNormalDbByCurProductCode(dbCntInfo,sourcetable,desttable,selectsql,insertsql)
    print("trade work day finish get data!")
    return



if __name__ == "__main__":

    # xmlfile = "E:\\pydevproj\\stockmarket\\finance\\resource\\finance.xml"
    # xmlfile = "F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    # dbCntInfo = dbcnt.DbCnt(xmlfile)
    dbCntInfo = dbcnt.createDbConnect(dbpool=False)
    # getProductBasicInfo(dbCntInfo)
    getaddtradecalendar(dbCntInfo)
