# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

# 表名:逻辑名 与finance.xml的逻辑名一致
LOGICNAME_TMPBASE = "tmpbase"
LOGICNAME_DBBASE = "dbbase"
LOGICNAME_TRADE = "traden"
TABLEDICT = {"stock_basics": LOGICNAME_TMPBASE,
             "productbasicinfo": LOGICNAME_DBBASE,
             "histtradedata": LOGICNAME_TMPBASE,
             "producttradedata": LOGICNAME_TRADE,
             "trade_cal":LOGICNAME_TMPBASE,
             "stock_basics_tspro":LOGICNAME_TMPBASE,
             "profit_divis":LOGICNAME_TMPBASE}

PRODUCTBASICINFO_SQL = "SELECT DISTINCT a.code product_code, a.name product_name, '1' product_type, \
       '1' money_type, a.area product_area, a.industry product_industry, \
       a.name product_fullname, LEFT(a.code,3) market_type, '0' exchange_code, \
       'L' ipo_status,a.timeToMarket listed_date, 0 delisted_date \
  FROM stock_basics a"

PRODUCTBASICINFO_INSERTSQL = "insert into productbasicinfo(product_code,product_name,product_type, \
money_type, product_area, product_industry, \
product_fullname, market_type, exchange_code, \
ipo_status,listed_date,delisted_date) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

PRODUCTBASICINFO_GETSQL = "SELECT product_code, product_name, product_type, \
       money_type, product_area, product_industry, \
       product_fullname, market_type, exchange_code, \
       ipo_status,listed_date, delisted_date \
  FROM productbasicinfo \
 where ipo_status = 'N' "

COMPANYBALANCESHEET_SQL = ""
COMPANYBALANCESHEET_INSERTSQL = ""

PRODUCTMAXTRADEDATE_SQL = " select ifnull(max(trade_date),0) maxtradedate from %s where product_code = '%s' "
## 从tusharep中获取数据
PRODUCTHISTTRADEDATATUSHARE_SQL = " select %s product_code,a.date trade_date, a.open open_price,high high_price, close close_price,\
low low_price, volume product_volume,amount product_amount from histtradedata a "

## 从tusharepro中获取数据
PRODUCTHISTTRADEDATATUSHAREPRO_SQL = " select left(a.ts_code,6) product_code,a.trade_date trade_date, a.open open_price,a.high high_price, a.close close_price,\
a.low low_price, a.vol product_volume,a.amount product_amount from histtradedata a "

PRODUCTTRADEDATA_INSERTSQL = "insert into producttradedata(product_code,trade_date,open_price, \
high_price, close_price, low_price, \
product_volume, product_amount) values ( %s, %s, %s, %s, %s, %s, %s, %s)"
