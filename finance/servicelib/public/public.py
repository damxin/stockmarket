# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

'''
    提供公共的接口
'''

from finance.servicelib.processinit import dbcnt
from finance.util import SqlCons as sc
from finance.util import GlobalCons as gc
import pandas as pd
from datetime import date, timedelta


def getAllProductBasicInfo(dbCntInfo):
    '''
    返回所有的产品的基本信息，默认只返回依然上市的产品，退市的不返回
    :param dbCntInfo:
    :return:
    '''
    tableDbBase = dbCntInfo.getDBCntInfoByTableName("productbasicinfo")
    tableRetTuple = tableDbBase.execSelectSmallSql(sc.PRODUCTBASICINFO_GETSQL)
    if len(tableRetTuple) == 0:
        return
    return pd.DataFrame(tableRetTuple)

def getCurProductBasicInfoByProductCode(dbCntInfo, productcode):
    '''
    获取具体产品的基本信息
    :param dbCntInfo:
    :param productcode:
    :return:
    '''
    tableDbBase = dbCntInfo.getDBCntInfoByTableName("productbasicinfo")
    tableRetTuple = tableDbBase.execSelectSmallSql(sc.CURPRODUCTBASICINFO_GETSQL%productcode)
    if len(tableRetTuple) == 0:
        return
    return pd.DataFrame(tableRetTuple).iloc[0]


'''
    20190102格式化为2019-01-02
'''


def dateSpecailFormat(intDateFormat):
    if intDateFormat < 10000000:
        print("date format is exception!", end="")
        print(intDateFormat)
        raise Exception("date format is exception!")
    strDate = ""
    strDate = strDate + intDateFormat / 10000 + "-"
    strDate = strDate + intDateFormat / 100 % 100 + "-"
    strDate = strDate + intDateFormat % 100
    return strDate


'''
    生成symbol代码标志
'''


def code_to_symbol(code):
    if code in gc.INDEX_LABELS:
        return gc.INDEX_LIST[code]
    else:
        if len(code) != 6:
            return code
        else:
            return '%s.sh' % code if code[:1] in ['5', '6', '9'] or code[:2] in ['11', '13'] else '%s.sz' % code

def getYesterday() -> int:
    '''
    返回昨日日期，比如20191010
    int :return:
    '''
    yesterday=int((date.today()-timedelta(days=1)).strftime("%Y%m%d"))
    return yesterday

def getnextnday(curdate,n) -> int:
    '''
    返回下一日日期，比如20191010
    int :return:
    '''
    import datetime
    y = int(curdate/10000)
    m = int(curdate/100%100)
    d = int(curdate%100)
    the_date = datetime.datetime(y, m, d)
    result_date = the_date + datetime.timedelta(days=n)
    nextnday = int(result_date.strftime("%Y%m%d"))
    return nextnday

def getTodayDate():
    '''
    返回今日日期，比如20191010
    int :return:
    '''
    todayday=int((date.today()).strftime("%Y%m%d"))
    return todayday

def listdictTypeChangeToDataFrame(datalistdict):
    '''
    list[dict]数据转换为dataframe，同时类型要正确转换
    :param datalistdict:
    :return:
    '''
    import pandas as pd
    import decimal
    datadf = pd.DataFrame(datalistdict)
    for keyname in datalistdict[0]:
        dictvalue = datalistdict[0][keyname]
        if isinstance(dictvalue,decimal.Decimal):
            datadf[keyname] = datadf[keyname].astype(float)
        elif isinstance(dictvalue,int):
            datadf[keyname] = datadf[keyname].astype(int)

    return datadf
