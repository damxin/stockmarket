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

def getMaxTradeTimeFromCurProdCode(dbCntInfo, productCode, kType = gc.K_DAY):
    '''
    获取已经存储在数据库中的最大值，如果是日以上级别则tradetime返回填写235959
    :param dbCntInfo:
    :param productCode:
    :param kType:gc.K_DAY 等
    :return: (tradeDate, tradeTime)
    '''

    tradeDate = 0

    sourceTable = ""
    execlsql = ""
    if kType in gc.K_DAY:
        sourceTable = "producttradedata"
        execlsql = "select max(trade_date) maxtradedate from %s where product_code = '%s' " % (sourceTable, productCode)
    elif kType in gc.K_30MIN:
        sourceTable = "prod30tradedata"
        symbolcode = code_to_symbol(productCode)
        execlsql = "select max(trade_date) maxtradedate from %s where symbol_code = '%s' " % (sourceTable, symbolcode)
    else:
        tradeDate = 20991231

    tableDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=sourceTable, productcode=productCode)

    tableRetListTuple = tableDbBase.execSelectSmallSql(execlsql)

    try :
        if tableRetListTuple is None:
            tradeDate = 19000101
        else:
            tradeDate = tableRetListTuple[0]['maxtradedate']
    except Exception as e:
        print(execlsql)
        # print(productCode, end='')
        print(type(tableRetListTuple))
        # print(productCode, end='')
        print(tableRetListTuple)
        # print(tableRetTuple[0]['maxtradedate'])
        print(e)


    return (tradeDate, 235959)

def getMaxTradeDateFromCurProductCode(dbCntInfo, productCode) -> int:
    '''
    获取产品代码在数据库中存储的最大交易日期
    :param dbCntInfo:
    :param productCode:
    :return:
    '''

    sourcetable = "producttradedata"
    tableDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=sourcetable, productcode=productCode)
    execlsql = "select max(trade_date) maxtradedate from producttradedata where product_code = '%s' " % productCode
    tableRetTuple = tableDbBase.execSelectSmallSql(execlsql)
    print(productCode, end='')
    print(type(tableRetTuple))
    print(productCode, end='')
    print(tableRetTuple)
    # print(tableRetTuple[0]['maxtradedate'])
    maxDate = 19000101 if tableRetTuple[0]['maxtradedate'] is None else tableRetTuple[0]['maxtradedate']

    # print(maxDate)
    return maxDate


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
        selectsql = selectsql + sc.PRODUCTBASICINFO_GETSQL + " where ipo_status = '%s' " % ipostatus
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
    tableRetTuple = tableDbBase.execSelectSmallSql(sc.CURPRODUCTBASICINFO_GETSQL % productcode)
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


def code_to_symbol(code):
    '''
        生成symbol代码标志
    '''
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
    yesterday = int((date.today() - timedelta(days=1)).strftime("%Y%m%d"))
    return yesterday


def getnextnday(curdate, n) -> int:
    '''
    返回下一日日期，比如20191010
    int :return:
    '''
    import datetime
    y = int(curdate / 10000)
    m = int(curdate / 100 % 100)
    d = int(curdate % 100)
    the_date = datetime.datetime(y, m, d)
    result_date = the_date + datetime.timedelta(days=n)
    nextnday = int(result_date.strftime("%Y%m%d"))
    return nextnday


def getTodayDate():
    '''
    返回今日日期，比如20191010
    int :return:
    '''
    todayday = int((date.today()).strftime("%Y%m%d"))
    return todayday

def getlastworkday():
    '''
    获取最近的工作日
    :return:
    '''
    import time

    finanalWorkDate = getTodayDate()
    curHour = time.localtime().tm_hour
    if curHour < 17:
        finanalWorkDate = getYesterday()
    # select max(trade_date) from openday where trade_date < %d
    selectsql = "select ifnull(max(trade_date),0) maxworkdate from openday where trade_flag = '1' and trade_date <= %d"% finanalWorkDate
    dbopenday = dbcnt.getDBCntInfoByTableName("openday")
    retresult = dbopenday.execSelectSmallSql(selectsql)
    return retresult[0]['maxworkdate']

def getlastyear():
    '''
    返回去年日期，比如现在20191010，则返回20181010
    int :return:
    '''
    todayday = int((date.today()).strftime("%Y%m%d"))
    lastday = (int(todayday / 10000) - 1) * 10000 + todayday % 10000
    return lastday

def gettimediff(srcdate, srctime, destdate, destime, kline='D'):
    '''

    :param srcdate: 20100901
    :param srctime: 1209   001209
    :param destdate:  20110902
    :param destime:  0900 000900
    :param kline:  日线级别，60分钟级别
    :return:
    '''
    import time
    import datetime

    dttm1 = datetime.datetime(int(srcdate/10000), (int(srcdate/100))%100, int(srcdate%100), int(srctime/10000), (int(srctime/100))%100, int(srcdate%100))
    dttm2 = datetime.datetime(int(destdate/10000), (int(destdate/100))%100, int(destdate%100), int(destime/10000), (int(destime/100))%100, int(destime%100))


    tm1 = time.mktime(dttm1.timetuple())
    tm2 = time.mktime(dttm2.timetuple())
    if kline in 'D':
        return int(tm2 - tm1)/3600
    else :
        return int(tm2 - tm1)



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
        if isinstance(dictvalue, decimal.Decimal):
            datadf[keyname] = datadf[keyname].astype(float)
        elif isinstance(dictvalue, int):
            datadf[keyname] = datadf[keyname].astype(int)

    return datadf


def insertNormalDbByCurProductCode(dbCntInfo, sourcetable, desttable, selectsql, insertsql, productcode=None):
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


def getcompanyfinancedata(dbcntinfo, product_code, compfinancetblname, datatype, datalength=5) -> pd.DataFrame:
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
        raise ValueError(
            "the param of function getcompanyfinancedata(%s) is error!\n please check!" % compfinancetblname)
    if datatype is not "Y" and datatype is not "Q":
        raise ValueError(
            "the param of function getcompanyfinancedata datatype(%s) is error!\n please check!" % datatype)

    dbSqlSession = dbcntinfo.getDBCntInfoByTableName(compfinancetblname, product_code)
    allDataGetSql = ""
    if datatype is "Y":
        companyfinacepubselsql = sc.COMPANYFINANCE_PUBYEARSELECTSQL[compfinancetblname]
        allDataGetSql = companyfinacepubselsql % (product_code, product_code, product_code, datalength)
        print("getcompanyfinancedata get sql:" + allDataGetSql)
    elif datatype is "Q":
        companyfinacepubselsql = sc.COMPANYFINANCE_PUBQUARTSELECTSQL[compfinancetblname]
        allDataGetSql = companyfinacepubselsql % (product_code, product_code, datalength)
        print("getcompanyfinancedata get sql:" + allDataGetSql)
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
    for dataindex in range(dataLength - 1):
        rateList.append(float(int((dataList[dataindex + 1] - dataList[dataindex]) / dataList[dataindex] * 10000) / 100))
    return rateList


def downloadloginsorupd(dbcnt, productcode, eventtype, dealstatus, sourcetype):
    '''
    表datadownloadlog日志记录插入或者更新
    :param dbcnt: 数据库的连接
    :param productcode:
    :param eventtype: 1.交易数据 2.Income  3.Balancesheet 4.Cashflow
    :param dealstatus: 0.准备开始 1.下载完成 2.导入正式表完成
    :param sourcetype: 0.各自下载 1.批量下载
    :return: True：成功，False：失败
    '''
    import time
    if productcode is None:
        raise ValueError("productcode do not valid value!")
        return False
    sqlsession = dbcnt.getDBCntInfoByTableName("datadownloadlog", productcode)

    logdate = int((date.today()).strftime("%Y%m%d"))
    datadownloadlogsql = sc.DATADOWNLOG_GETDATA % (productcode, eventtype, sourcetype, logdate)
    datalogexistlist = sqlsession.execSelectAllSql(datadownloadlogsql)
    keyname = "product_code"
    cntnum = datalogexistlist[0][keyname]
    # 有数据现在做更新
    if cntnum > 0:
        datadownloadlogupdsql = sc.DATADOWNLOG_UPDATEDATA % (dealstatus, productcode, eventtype, sourcetype, logdate)
        sqlsession.execUpdateOrDelSql(datadownloadlogupdsql)
    else:
        logtime = int(time.strftime('%H:%M:%S', time.localtime(time.time())))
        datadownloadloginssql = sc.DATADOWNLOG_INSERTDATA % (
            productcode, eventtype, dealstatus, sourcetype, logdate, logtime)
        sqlsession.execNotSelectSql(datadownloadloginssql)

    return True


def getCpuCount():
    '''
    返回机器cpu个数
    :return:
    '''
    from multiprocessing import cpu_count
    print("cpu个数(%d)" % cpu_count())
    return cpu_count()


def getRealTableName(tableName, productCode):
    '''
    对于分表进行真实表的拼接
    :param tableName:
    :param productCode:
    :return:
    '''
    if tableName not in sc.SPLITTBLDICT:
        return None

    strlength = len(productCode)
    modelnum = int(productCode[strlength - 2:])
    resultnum = modelnum % sc.SPLITTBLDICT[tableName]
    resultnum = 32 if resultnum == 0 else resultnum
    strresult = str(resultnum)
    realtablename = tableName + strresult.zfill(2)

    return realtablename

def code_to_symbol(productcode):
    '''
    返回symbol标志
    :param productcode:
    :return:
    '''
    from finance.util import GlobalCons as gc

    if productcode in gc.INDEX_LABELS:
        return gc.INDEX_LIST[productcode]
    else:
        if len(productcode) != 6 :
            return productcode
        else:
            return 'sh%s'%productcode if productcode[:1] in ['5', '6', '9'] or productcode[:2] in ['11', '13'] else 'sz%s'%productcode

