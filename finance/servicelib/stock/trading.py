# -*- coding:utf-8 -*-
import tushare as ts
from sqlalchemy import create_engine
from finance.dbsql import mysqldatabase as msqldatabase

def getAllBaseData():
    df = ts.get_stock_basics()
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1/stocknotdealmarket?charset=utf8')
    df.to_sql('stock_basics', engine, if_exists="replace", index=False)
    print("finish")

def getProductBasicInfo():
    msqldatabase.MysqlDatabase mysqldatabase = msqldatabase.MysqlDatabase("127.0.0.1","3306","root","root","stockmarket")
    mysqldatabase.getConnection()