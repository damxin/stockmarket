# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

import tushare as ts
from sqlalchemy import create_engine
from finance.dbsql import mysqldatabase

def getAllBaseData(filedata):
    df = ts.get_stock_basics()
    basicdf = df.reset_index(drop=False)
    # print(df)
    # print("df finish")
    # print(df.reset_index(drop=False))
    # print(df.reset_index(drop=False), file=filedata)
    # for index, row in df.iterrows():
    #     print(index, file=filedata, end="")
    #     print(row,file=filedata)
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1/stocknotdealmarket?charset=utf8')
    basicdf.to_sql('stock_basics', engine, if_exists="replace", index=False)
    print("finish")

def getProductBasicInfo():
    mysqldbase = mysqldatabase.MysqlDatabase("127.0.0.1","3306","root","root","stockmarket")
    mysqldbase.getConnection()
    mysqldbase.closeDBConnect()

if __name__ == "__main__":
    filedata = open(".\stock_basics.txt", 'w+')
    # getAllBaseData(filedata)
    getProductBasicInfo()
    filedata.close()