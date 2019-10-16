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
    # 建立连接与tusharepro
    pro = ts.pro_api('00f0c017db5d284d992f78f0971c73c9ecba4aa03dee2f38e71e4d9c')
    df = pro.trade_cal(exchange=exchange_code)
    basicdf = df.reset_index(drop=False)
    tablename = 'trade_cal'
    engine = dbCntInfo.getEngineByTableName(tablename)
    basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
    print("finish")


'''
    工作日追加
'''
def getaddtradecalendar(exchange_code):
   return



if __name__ == "__main__":

    xmlfile = "E:\\pydevproj\\stockmarket\\finance\\resource\\finance.xml"
    #     xmlfile = "F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    dbCntInfo = dbcnt.DbCnt(xmlfile)
    # getProductBasicInfo(dbCntInfo)
    getTradeCalendar(dbCntInfo)
