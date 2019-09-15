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

def getStockBasics(dbCntInfo,filedata):
    df = ts.get_stock_basics()
    basicdf = df.reset_index(drop=False)
    tablename = 'stock_basics'
    engine = dbCntInfo.getEngineByTableName(tablename)
    basicdf.to_sql(tablename, engine, if_exists="replace", index=False)
    print("finish")
'''
    数据插入到表product_basic_info中
'''
def getProductBasicInfo(dbCntInfo):
    dbCntInfo.getDbCnt()

    mysqldbase = mysqldatabase.MysqlDatabase("127.0.0.1","3306","root","root","stockmarket")
    mysqldbase.getConnection()
    mysqldbase.closeDBConnect()

if __name__ == "__main__":
    filedata = open(".\stock_basics.txt", 'w+')
    xmlfile = "F:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    dbCntInfo = dbcnt.DbCnt(xmlfile)
    getAllBaseData(dbCntInfo,filedata)
    getProductBasicInfo()
    filedata.close()