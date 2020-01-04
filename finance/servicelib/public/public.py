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


def getAllProductBasicInfo(dbCntInfo, ipostatus=None):
    '''
    返回所有的产品的基本信息，默认只返回依然上市的产品，退市的不返回
    :param dbCntInfo:
    :param ipostatus A:所有产品信息 N:正常上市
    :return:
    '''
    ipostatus = ipostatus if ipostatus is not None else "N"
    tableDbBase = dbCntInfo.getDBCntInfoByTableName("productbasicinfo")
    selectsql = ""
    if ipostatus in "A":
        selectsql = selectsql + sc.PRODUCTBASICINFO_GETSQL
    else:
        selectsql = selectsql + sc.PRODUCTBASICINFO_GETSQL + " where ipo_status = '%s' "%ipostatus
    tableRetListDict = tableDbBase.execSelectSmallSql(selectsql)
    if len(tableRetListDict) == 0:
        return
    return pd.DataFrame(tableRetListDict)

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


def dateSpecailFormat(intDateFormat):
    '''
    20190102格式化为2019-01-02
    :param intDateFormat:
    :return:
    '''
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

def insertNormalDbByCurProductCode(dbCntInfo,sourcetable,desttable,selectsql,insertsql,productcode=None):
    '''
    source表中数据批量插入到正式库中
    :param productcode:可为None
    :param dbCntInfo:
    :param sourcetable:
    :param desttable:
    :param selectsql:
    :param insertsql:
    :return:
    '''
    sourceDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=sourcetable, productcode=productcode)
    destDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=desttable, productcode=productcode)
    while (True):
        sourceRetList = sourceDbBase.execSelectManySql(selectsql)
        if len(sourceRetList) == 0:
            break
        # 数据插入到另外一个库里面
        sourceList = []
        for oneList in sourceRetList:
            sourceList.append(tuple(oneList.values()))
        destDbBase.execInsertManySql(insertsql, sourceList)

def getcompanyfinancedata(dbcntinfo,product_code,compfinancetblname,datatype,datalength=5) -> pd.DataFrame:
    '''
    company_income,company_cashflow,company_balance_sheet数据获取
    :param dbcntinfo 数据库连接
    :param compfinancetblname:company_income,company_cashflow,company_balance_sheet
    :param product_code: None则报错，只支持单一产品数据获取
    :param datatype:Y:年，Q:季度
    :param datalength默认值为5，显示5年，季度就没有日期了。
    :return:DataFrame (product_code,......)
    '''

    if product_code is None or datatype is None:
        raise ValueError("the param of function getcompanyfinancedata(%s) is error!\n please check!"%compfinancetblname)
    if datatype is not "Y" and datatype is not "Q":
        raise ValueError(
            "the param of function getcompanyfinancedata datatype(%s) is error!\n please check!" % datatype)

    dbSqlSession = dbcntinfo.getDBCntInfoByTableName(compfinancetblname, product_code)
    allDataGetSql=""
    if datatype is "Y":
        companyfinacepubselsql = sc.COMPANYFINANCE_PUBYEARSELECTSQL[compfinancetblname]
        allDataGetSql = companyfinacepubselsql % (product_code,product_code,product_code,datalength)
        print("getcompanyfinancedata get sql:" + allDataGetSql)
    elif datatype is "Q":
        companyfinacepubselsql = sc.COMPANYFINANCE_PUBQUARTSELECTSQL[compfinancetblname]
        allDataGetSql = companyfinacepubselsql % (product_code, product_code, datalength)
        print("getcompanyfinancedata get sql:"+allDataGetSql)
    tradeDataTupleInList = dbSqlSession.execSelectAllSql(allDataGetSql)
    dfdata = listdictTypeChangeToDataFrame(tradeDataTupleInList)

    return dfdata

def getRateNextToByList(dataList) -> list:
    '''
    对传入的list计算rate，计算公式(下一个值-当前值)/当前值,以百分比表示,保留2位小数
    :param dataList:
    :return:
    '''
    rateList = []
    dataLength = len(dataList)
    for dataindex in range(dataLength-1):
        rateList.append(float(int((dataList[dataindex+1]-dataList[dataindex])/dataList[dataindex]*10000)/100))
    return rateList

def downloadloginsorupd(dbcnt,productcode,eventtype,dealstatus,sourcetype):
    '''
    表datadownloadlog日志记录插入或者更新
    :param dbcnt: 数据库的连接
    :param productcode:
    :param eventtype: 1.交易数据 2.Income  3.Balancesheet 4.Cashflow
    :param dealstatus: 0.准备开始 1.下载完成 2.导入正式表完成
    :param sourcetype: 0.各自下载 1.批量下载
    :return: True：成功，False：失败
    '''
    if productcode is None:
        raise  ValueError("productcode do not valid value!")
        return False
    sqlsession = dbcnt.getDBCntInfoByTableName("datadownloadlog", productcode)

    logdate = int((date.today()).strftime("%Y%m%d"))
    datadownloadlogsql = sc.DATADOWNLOG_GETDATA %(productcode,eventtype,sourcetype,logdate)
    datalogexistlist = sqlsession.execSelectAllSql(datadownloadlogsql)
    keyname = "product_code"
    cntnum = datalogexistlist[0][keyname]
    # 有数据现在做更新
    if cntnum > 0 :
        datadownloadlogupdsql = sc.DATADOWNLOG_UPDATEDATA %(dealstatus,productcode,eventtype,sourcetype,logdate)
        sqlsession.execUpdateOrDelSql(datadownloadlogupdsql)
    else :
        logtime = int(time.strftime('%H:%M:%S',time.localtime(time.time())))
        datadownloadloginssql = sc.DATADOWNLOG_INSERTDATA %(productcode,eventtype,dealstatus,sourcetype,logdate,logtime)
        sqlsession.execNotSelectSql(datadownloadloginssql)

    return True

