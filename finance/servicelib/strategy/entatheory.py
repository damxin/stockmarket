# -*- coding:utf-8 -*-
'''
   缠论的具体实现
'''

import logging
import pandas as pd
from finance.servicelib.public import public as pb
from finance.servicelib.processinit import dbcnt
from finance.util import SqlCons as sc
from finance.util import GlobalCons as gc

from finance.servicelib.processinit import stocklog


# 实现日线级别的画法。

class EntangLingTheory():

    def __init__(self, prodCode):
        self.prod_code = prodCode

    def inclusionrRelotionDeal(self, tradeDataList):
        '''
        依据入参，包含关系处理，然后写入数据库分表entdaytradedata中
        :param tradeDataList:
        :return: DataFrame
        '''
        lastTradeData = {}
        firstTradeDataFlag = True
        trendUpOrDown = gc.TRENDFLAG_UP

        logging.info("inclusionrRelotionDeal productcode(%s) begin"%self.prod_code)
        srcTable = "entdaytradedata"
        realTblName = pb.getRealTableName(srcTable, self.prod_code)
        dbCntInfo = dbcnt.getDBCntInfoByTableName(srcTable, self.prod_code)
        insertSql = sc.ENTDAYTRADEDATA_INSERT % realTblName
        datainsertsql = insertSql
        insertdatacnt = 0
        # 默认上市的第一天是上涨走势,因为不可能比原始股更便宜了，包含关系处理
        for curOneTradeData in tradeDataList:
            if firstTradeDataFlag:
                lastTradeData[gc.TRADEDATEKEY] = int(curOneTradeData[gc.TRADEDATEKEY])
                lastTradeData[gc.OPENPRICEKEY] = curOneTradeData[gc.HIGHPRICEKEY]
                lastTradeData[gc.HIGHPRICEKEY] = curOneTradeData[gc.HIGHPRICEKEY]
                lastTradeData[gc.CLOSEPRICEKEY] = curOneTradeData[gc.LOWPRICEKEY]
                lastTradeData[gc.LOWPRICEKEY] = curOneTradeData[gc.LOWPRICEKEY]
                lastTradeData[gc.MERGEFLAGKKEY] = '0'
                firstTradeDataFlag = False
                continue

            # 判断是否包含 左包含右，或者右包含左的K线
            # 左包含右
            if lastTradeData[gc.HIGHPRICEKEY] >= curOneTradeData[gc.HIGHPRICEKEY] and lastTradeData[gc.LOWPRICEKEY] <= \
                    curOneTradeData[gc.LOWPRICEKEY]:
                if trendUpOrDown == gc.TRENDFLAG_UP:
                    # 高高取高，低低取高
                    lastTradeData[gc.LOWPRICEKEY] = curOneTradeData[gc.LOWPRICEKEY]
                    lastTradeData[gc.CLOSEPRICEKEY] = curOneTradeData[gc.LOWPRICEKEY]
                else:  # trendUpOrDown == gc.TRENDFLAG_DOWN
                    # 高高取低，低低取低
                    lastTradeData[gc.HIGHPRICEKEY] = curOneTradeData[gc.HIGHPRICEKEY]
                    lastTradeData[gc.OPENPRICEKEY] = curOneTradeData[gc.HIGHPRICEKEY]
                lastTradeData[gc.MERGEFLAGKKEY] = '1'
                lastTradeData[gc.TRADEDATEKEY] = curOneTradeData[gc.TRADEDATEKEY]

            elif lastTradeData[gc.HIGHPRICEKEY] <= curOneTradeData[gc.HIGHPRICEKEY] and lastTradeData[gc.LOWPRICEKEY] >= \
                    curOneTradeData[gc.LOWPRICEKEY]:
                if trendUpOrDown == gc.TRENDFLAG_UP:
                    # 高高取高，低低取高
                    lastTradeData[gc.HIGHPRICEKEY] = curOneTradeData[gc.HIGHPRICEKEY]
                    lastTradeData[gc.OPENPRICEKEY] = curOneTradeData[gc.HIGHPRICEKEY]
                else:  # trendUpOrDown == gc.TRENDFLAG_DOWN
                    # 高高取低，低低取低
                    lastTradeData[gc.LOWPRICEKEY] = curOneTradeData[gc.LOWPRICEKEY]
                    lastTradeData[gc.OPENPRICEKEY] = curOneTradeData[gc.LOWPRICEKEY]
                lastTradeData[gc.MERGEFLAGKKEY] = '1'
                lastTradeData[gc.TRADEDATEKEY] = curOneTradeData[gc.TRADEDATEKEY]

            else:  # 无包含关系
                if gc.MERGEFLAGKKEY not in lastTradeData:
                    lastTradeData[gc.MERGEFLAGKKEY] = '0'
                # lastTradeData数据插入到数据库中的entdaytradedata表中

                if insertdatacnt == 100:
                    insertResult = dbCntInfo.execNotSelectSql(datainsertsql[:-1])
                    if insertResult is not None:
                        print("异常语句:" + datainsertsql[:-1])
                        raise Exception("数据库插入异常!")  # 异常被抛出，print函数无法执行
                    datainsertsql = insertSql
                    insertdatacnt = 0
                # product_code, trade_date,open_price,high_price,close_price,low_price,merge_flag,updown_flag
                insertdatacnt = insertdatacnt + 1
                datainsertsql = datainsertsql + sc.ENTDAYTRADEDATA_INSERTDATA % (
                    self.prod_code, lastTradeData[gc.TRADEDATEKEY], lastTradeData[gc.OPENPRICEKEY],
                    lastTradeData[gc.HIGHPRICEKEY], lastTradeData[gc.CLOSEPRICEKEY],
                    lastTradeData[gc.LOWPRICEKEY], lastTradeData[gc.MERGEFLAGKKEY],
                    "N")
                # 这边需要调整为每200条插入一次
                # 趋势判断
                if lastTradeData[gc.HIGHPRICEKEY] > curOneTradeData[gc.HIGHPRICEKEY]:
                    trendUpOrDown = gc.TRENDFLAG_DOWN
                else:
                    trendUpOrDown = gc.TRENDFLAG_UP
                # 数据赋值
                lastTradeData[gc.TRADEDATEKEY] = int(curOneTradeData[gc.TRADEDATEKEY])
                lastTradeData[gc.OPENPRICEKEY] = curOneTradeData[gc.HIGHPRICEKEY]
                lastTradeData[gc.HIGHPRICEKEY] = curOneTradeData[gc.HIGHPRICEKEY]
                lastTradeData[gc.CLOSEPRICEKEY] = curOneTradeData[gc.LOWPRICEKEY]
                lastTradeData[gc.LOWPRICEKEY] = curOneTradeData[gc.LOWPRICEKEY]
                lastTradeData[gc.MERGEFLAGKKEY] = '0'

        if insertdatacnt > 0:
            insertResult = dbCntInfo.execNotSelectSql(datainsertsql[:-1])
            if insertResult is not None:
                print("异常语句:" + datainsertsql[:-1])
                raise Exception("数据库插入异常!")  # 异常被抛出，print函数无法执行

        logging.info("inclusionrRelotionDeal productcode(%s) finish" % self.prod_code)
        return None

    def upDownStatusGet(self, prod_code, srcTable="entdaytradedata", beginDate=0):
        '''
        伪顶底分型初步判断
        :param srcTable: 一般为entdaytradedata
        :param beginDate:一般为0
        :return:
        '''
        realTblName = pb.getRealTableName(srcTable, prod_code)
        updatetblsql = sc.ENTDAYTRADEDATA_UPDATETBL%realTblName
        updateupdownflagsql = updatetblsql + sc.ENTDAYTRADEDATA_UPDATEUUPDOWNFLAG
        dbCntInfo = dbcnt.getDBCntInfoByTableName(srcTable, prod_code)
        # product_code, trade_date,open_price,high_price,close_price,low_price,merge_flag,updown_flag
        selectSql = sc.ENTDAYTRADEDATA_GET % (realTblName, prod_code, beginDate)
        entdayTrDataList = dbCntInfo.execSelectAllSql(selectSql)
        if len(entdayTrDataList) == 0:
            return None
        logging.info("upDownStatusGet productcode(%s) begin" % prod_code)
        entdayTrDataDf = pd.DataFrame(entdayTrDataList)

        curEntdayTrDataDf = entdayTrDataDf.set_index("trade_date")
        # print(curEntdayTrDataDf)
        # print(curEntdayTrDataDf.close_price.diff())
        # 按照日期进行升序排序后，从负到正为底分型，从正到负为顶分型。
        # 线段的顶底也是最初的伪顶底中的一种。

        # 一维数组
        resultSeries = curEntdayTrDataDf.close_price.diff()
        print(type(resultSeries))
        firstIndex = 0
        lastTradeDate = 0
        lastCloseDiff = 0
        updownFlag = ""
        updownflaglist = []
        listnumcnt  = 0
        for curTradeDate, curDiffCloseData in resultSeries.items():
            # lastStatus = curTradeData
            # print(curDiffCloseData)
            if firstIndex == 0:
                firstIndex = 1
                updownFlag = gc.NORMALTYPING
                lastTradeDate = curTradeDate
                lastCloseDiff = curDiffCloseData
                continue
            # 第一个数据需要特殊处理
            if firstIndex == 1:
                if curDiffCloseData < 0:
                    updownFlag = gc.UPTYPING
                else:
                    updownFlag = gc.DOWNTYPING
            else:
                # 从负到正为底分型
                if lastCloseDiff < 0 and curDiffCloseData > 0:
                    updownFlag = gc.DOWNTYPING
                # 从正到负为顶分型
                elif lastCloseDiff > 0 and curDiffCloseData < 0:
                    updownFlag = gc.UPTYPING

            # 更改数据库lastTradeDate天的数据顶底状态
            if updownFlag not in gc.NORMALTYPING:
                if listnumcnt == gc.COUNTNUM:
                    updateResult = dbCntInfo.execupdatemanysql(updateupdownflagsql, updownflaglist)
                    if updateResult is not None:
                        print("异常语句:" + updateupdownflagsql)
                        raise Exception("数据库更新异常!")  # 异常被抛出，print函数无法执行
                    listnumcnt = 0
                    updownflaglist.clear()
                listnumcnt = listnumcnt + 1
                updownflaglist.append((updownFlag,prod_code,lastTradeDate))

            firstIndex = firstIndex + 1
            updownFlag = gc.NORMALTYPING
            lastTradeDate = curTradeDate
            lastCloseDiff = curDiffCloseData
        if listnumcnt > 0:
            updateResult = dbCntInfo.execupdatemanysql(updateupdownflagsql, updownflaglist)
            if updateResult is not None:
                print("异常语句:" + updateupdownflagsql)
                raise Exception("数据库更新异常!")  # 异常被抛出，print函数无法执行
        logging.info("upDownStatusGet productcode(%s) finish" % prod_code)
        return None

    def apicalOrBasicGet(self, srcTable, prod_code):
        '''
        笔对应的顶底分型判断
        :param srcTable:
        :param prod_code:
        :return:
        '''
        logging.info("apicalOrBasicGet productcode(%s) begin" % prod_code)
        realTblName = pb.getRealTableName(srcTable, prod_code)
        dbCntInfo = dbcnt.getDBCntInfoByTableName(srcTable, prod_code)
        # product_code, trade_date,open_price,high_price,close_price,low_price,merge_flag,updown_flag
        # 获取最近的A或者B的交易日期数据。
        selectSql = sc.ENTDAYTRADEDATA_LASTAORBGET % (realTblName, prod_code, realTblName, prod_code)
        entdayTrDataList = dbCntInfo.execSelectAllSql(selectSql)
        if len(entdayTrDataList) == 0:
            print("no data will be deal!")
            logging.info("apicalOrBasicGet productcode(%s) finish eraly" % prod_code)
            return
        entdayTrDataDf = pd.DataFrame(entdayTrDataList)
        curEntdayTrDataDf = entdayTrDataDf.set_index(gc.TRADEDATEKEY)
        # print(curEntdayTrDataDf)
        lastStatus = gc.NORMALTYPING
        # 不算头，不算尾，中间有3条，则即可成笔。
        curMiddleCount = 0
        realApicalBasicFlagIndex = -1
        highOrLowPrice = 0
        realApicalBasicFlagList = []
        for tradeDateIndex, curUpDownData in curEntdayTrDataDf.iterrows():
            # 不存在Apical/Basic，或者数据的首条记录就是Apical/Basic
            if curUpDownData[gc.UPDOWNFLAGKEY] == gc.UPTYPING and lastStatus != curUpDownData[gc.UPDOWNFLAGKEY]:
                # 不存在Apical/Basic
                if lastStatus in gc.NORMALTYPING:
                    realApicalBasicFlagList.append({tradeDateIndex: gc.APICALTYPING})
                    curMiddleCount = 0
                    lastStatus = gc.APICALTYPING
                    realApicalBasicFlagIndex = realApicalBasicFlagIndex + 1
                    highOrLowPrice = curUpDownData[gc.HIGHPRICEKEY]
                # 上一个是暂时认为的底,那么这个可以认为是顶
                elif lastStatus in gc.BASETYPING and curMiddleCount > 2:
                    realApicalBasicFlagList.append({tradeDateIndex: gc.APICALTYPING})
                    lastStatus = gc.APICALTYPING
                    curMiddleCount = 0
                    realApicalBasicFlagIndex = realApicalBasicFlagIndex + 1
                    highOrLowPrice = curUpDownData[gc.HIGHPRICEKEY]
                    # print("%d的日期%d为顶，金额为%f" % (realApicalBasicFlagIndex, tradeDateIndex, highOrLowPrice))
                # 存在更高的顶
                elif lastStatus in gc.APICALTYPING and highOrLowPrice < curUpDownData[gc.HIGHPRICEKEY]:
                    realApicalBasicFlagList.pop(realApicalBasicFlagIndex)
                    realApicalBasicFlagList.append({tradeDateIndex: gc.APICALTYPING})
                    curMiddleCount = 0
                    highOrLowPrice = curUpDownData[gc.HIGHPRICEKEY]
                    # print("%d的日期%d修正为更高的顶，金额为%f" % (realApicalBasicFlagIndex, tradeDateIndex, highOrLowPrice))

            elif curUpDownData[gc.UPDOWNFLAGKEY] == gc.DOWNTYPING and lastStatus != curUpDownData[gc.UPDOWNFLAGKEY]:
                # 不存在Apical/Basic
                if lastStatus in gc.NORMALTYPING:
                    realApicalBasicFlagList.append({tradeDateIndex: gc.BASETYPING})
                    curMiddleCount = 0
                    lastStatus = gc.BASETYPING
                    realApicalBasicFlagIndex = realApicalBasicFlagIndex + 1
                    highOrLowPrice = curUpDownData[gc.LOWPRICEKEY]
                # 上一个是暂时认为的顶,那么这个可以认为是底
                elif lastStatus in gc.APICALTYPING and curMiddleCount > 2:
                    realApicalBasicFlagList.append({tradeDateIndex: gc.BASETYPING})
                    lastStatus = gc.BASETYPING
                    curMiddleCount = 0
                    realApicalBasicFlagIndex = realApicalBasicFlagIndex + 1
                    highOrLowPrice = curUpDownData[gc.LOWPRICEKEY]
                    # print("%d的日期%d为底，金额为%f" % (realApicalBasicFlagIndex, tradeDateIndex, highOrLowPrice))
                # 存在更低的D
                elif lastStatus in gc.BASETYPING and highOrLowPrice > curUpDownData[gc.LOWPRICEKEY]:
                    realApicalBasicFlagList.pop(realApicalBasicFlagIndex)
                    realApicalBasicFlagList.append({tradeDateIndex: gc.BASETYPING})
                    curMiddleCount = 0
                    highOrLowPrice = curUpDownData[gc.LOWPRICEKEY]
                    # print("%d的日期%d修正为更低的底，金额为%f" % (realApicalBasicFlagIndex, tradeDateIndex, highOrLowPrice))
            elif curUpDownData[gc.UPDOWNFLAGKEY] == gc.APICALTYPING and lastStatus != curUpDownData[gc.UPDOWNFLAGKEY]:
                lastStatus = gc.APICALTYPING

                curMiddleCount = 0
                highOrLowPrice = curUpDownData[gc.HIGHPRICEKEY]
            elif curUpDownData[gc.UPDOWNFLAGKEY] == gc.BASETYPING and lastStatus != curUpDownData[gc.UPDOWNFLAGKEY]:
                lastStatus = gc.BASETYPING

                curMiddleCount = 0
                highOrLowPrice = curUpDownData[gc.LOWPRICEKEY]
            else:
                curMiddleCount = curMiddleCount + 1
        # 最后一笔由于还未经过后面的验证，不能认为是顶或者底
        if realApicalBasicFlagIndex >= 0:
            realApicalBasicFlagList.pop(realApicalBasicFlagIndex)
            realApicalBasicFlagIndex = realApicalBasicFlagIndex - 1
            # print("%d这条暂时不能认为是顶或者底" % (realApicalBasicFlagIndex + 1))
        # print(realApicalBasicFlagList)
        # 根据realApicalBasicFlagList进行顶或者底的更新
        updatetblsql = sc.ENTDAYTRADEDATA_UPDATETBL%realTblName
        updateabflagsql = updatetblsql + sc.ENTDAYTRADEDATA_UPDATEUUPDOWNFLAG
        updateablist = []
        for tmpTradeIndex in range(len(realApicalBasicFlagList)):
            # print(realApicalBasicFlagList[tmpTradeIndex])
            for oneTradeDate, upDownFlagValue in realApicalBasicFlagList[tmpTradeIndex].items():
                if len(updateablist) == gc.COUNTNUM:
                    updateResult = dbCntInfo.execupdatemanysql(updateabflagsql, updateablist)
                    if updateResult is not None:
                        print("异常语句:" + updateabflagsql)
                        raise Exception("数据库更新异常!")  # 异常被抛出，print函数无法执行
                    updateablist.clear()
                updateablist.append((upDownFlagValue, self.prod_code, oneTradeDate))

        if len(updateablist) > 0:
            updateResult = dbCntInfo.execupdatemanysql(updateabflagsql, updateablist)
            if updateResult is not None:
                print("异常语句:" + updateabflagsql)
                raise Exception("数据库更新异常!")  # 异常被抛出，print函数无法执行

        logging.info("apicalOrBasicGet productcode(%s) finish " % prod_code)
        return None

    def kLineMerge(self, klineType='D'):
        '''
         k线做合并，就是处理前后的包含关系，同时完成笔的顶分型和底分型判断，但是该判断里面不包含跳空处理。
        处理完毕后需要写入到表entdaytradedata01,entdaytradedata02,...entdaytradedata32
        :param klineType: F:5min, T:30min，S:60min， D:日，W:周，M:月，Y：年
        :return:
        '''

        klineType = gc.K_DAY if klineType is None else klineType
        tradeDataSql = ""

        # 从producttradedata读取数据
        if klineType == gc.K_DAY:
            # 获取已经插入的最大tradedate

            srcTable = "producttradedata"
            souceDbTrade = dbcnt.getDBCntInfoByTableName(srcTable, self.prod_code)
            tradeDataSql = sc.DAYTRADEDATA_GET % (self.prod_code, 0)

        tradeDataList = souceDbTrade.execSelectAllSql(tradeDataSql)
        print(type(tradeDataList))
        if len(tradeDataList) > 0:
            # 包含关系处理
            incResult = self.inclusionrRelotionDeal(tradeDataList)
            if incResult is not None:
                return incResult

        # 顶底分型判断,从对应的entdaytradedata表中获取数据。
        srcTable = "entdaytradedata"
        incResult = self.upDownStatusGet(self.prod_code, srcTable, 0)
        if incResult is not None:
            return incResult
        # 真实的顶底分型判断
        incResult = self.apicalOrBasicGet(srcTable, self.prod_code)
        if incResult is not None:
            return incResult
        # 画k线图，可以暂时不实现。
        return None

def futureKLine(logicname):
    '''

    :param databaseno: productdatabaserule的logicname的trade1,trade2,trade3
    :return:
    '''
    stocklog.initLogging(logicname)
    try:
        xmlfile = "G:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
        dbCntInfo = dbcnt.createDbConnect(xmlfile, dbpool=False)
        productBasicInfodf = pb.getAllProductBasicInfo(dbCntInfo, ipostatus='A')
        for rowIndex in productBasicInfodf.index:
            oneProductTuple = productBasicInfodf.iloc[rowIndex]
            productCode = oneProductTuple["product_code"]  ## 产品代码
            tradelogicname = dbCntInfo.getTradeLogicNameByProductCodeAndTradeDate(productCode, 0)
            if logicname not in tradelogicname:
                continue
            logging.info("%d productcode(%s) begin to deal" % (rowIndex, productCode))
            entangLingTheory = EntangLingTheory(productCode)
            resultret = entangLingTheory.kLineMerge(gc.K_DAY)
            if resultret is not None:
                break
            logging.info("productcode(%s) finish!" % productCode)
        print("future all finished!")
    finally:
        dbCntInfo.closeAllDBConnect()
    return None

from multiprocessing import Pool
from finance.servicelib.public import public as pb

if __name__ == "__main__":
    path = 'D:/software/new_haitong'


    # 按分库进行并发
    with Pool(3) as p:
        print(p.map(futureKLine, ["trade1", "trade2", "trade3"]))


