# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

PRODUCTBASICINFO_SQL="SELECT DISTINCT a.code product_code, a.name product_name, '1' product_type, \
       '1' money_type, a.area product_area, a.industry product_industry, \
       a.name product_fullname, LEFT(a.code,3) codeprethree, NULL exchange_code, \
       'L' ipo_status,a.`timeToMarket` listed_date, 0 delisted_date \
FROM stock_basics a"