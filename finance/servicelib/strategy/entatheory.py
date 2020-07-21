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

        logging.info("inclusionrRelotionDeal productcode(%s) begin" % self.prod_code)
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
                    "N", 0)
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
        tradeDataSql = sc.ENTDAYTRADEDATA_LASTAORBDATEGET % (realTblName, prod_code)
        souceDbTrade = dbcnt.getDBCntInfoByTableName(srcTable, prod_code)
        destRetList = souceDbTrade.execSelectSmallSql(tradeDataSql)
        maxtradedate = 0
        if len(destRetList) > 0:
            maxtradedate = destRetList[0]['maxtradedate']
            maxtradedate = maxtradedate - 1
        # update语句准备
        updatetblsql = sc.ENTDAYTRADEDATA_UPDATETBL % realTblName
        updateupdownflagsql = updatetblsql + sc.ENTDAYTRADEDATA_UPDATEUUPDOWNFLAG

        # 获取需要处理的数据
        dbCntInfo = dbcnt.getDBCntInfoByTableName(srcTable, prod_code)
        # product_code, trade_date,open_price,high_price,close_price,low_price,merge_flag,updown_flag
        selectSql = sc.ENTDAYTRADEDATA_GET % (realTblName, prod_code, maxtradedate, 0)
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
        # print(type(resultSeries))
        firstIndex = 0
        lastTradeDate = 0
        lastCloseDiff = 0
        updownFlag = ""
        updownflaglist = []
        listnumcnt = 0
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
                updownflaglist.append((updownFlag, prod_code, lastTradeDate))

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
        tradeDataSql = sc.ENTDAYTRADEDATA_LASTAORBDATEGET % (realTblName, prod_code)
        destRetList = dbCntInfo.execSelectSmallSql(tradeDataSql)
        maxtradedate = 0
        if len(destRetList) > 0:
            maxtradedate = destRetList[0]['maxtradedate']
            maxtradedate = maxtradedate - 1

        # product_code, trade_date,open_price,high_price,close_price,low_price,merge_flag,updown_flag
        # 获取最近的A或者B的交易日期数据。
        selectSql = sc.ENTDAYTRADEDATA_GET % (realTblName, prod_code, maxtradedate, 0)
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
        statusmodifyflag = False
        newhighprice = 0
        newlowprice = 0
        for tradeDateIndex, curUpDownData in curEntdayTrDataDf.iterrows():
            newhighprice = curUpDownData[gc.HIGHPRICEKEY]
            newlowprice = curUpDownData[gc.LOWPRICEKEY]
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
                    # statusmodifyflag = False
                    realApicalBasicFlagIndex = realApicalBasicFlagIndex + 1
                    highOrLowPrice = curUpDownData[gc.HIGHPRICEKEY]
                    logging.debug(
                        "%d is apical %d, price(%f)" % (realApicalBasicFlagIndex, tradeDateIndex, highOrLowPrice))
                # 存在更高的顶
                elif lastStatus in gc.APICALTYPING and highOrLowPrice < curUpDownData[gc.HIGHPRICEKEY]:
                    realApicalBasicFlagList.pop(realApicalBasicFlagIndex)
                    realApicalBasicFlagList.append({tradeDateIndex: gc.APICALTYPING})
                    curMiddleCount = 0
                    # statusmodifyflag = True
                    highOrLowPrice = curUpDownData[gc.HIGHPRICEKEY]
                    logging.debug("%d change apical date %d higher apical,price(%f)" % (
                        realApicalBasicFlagIndex, tradeDateIndex, highOrLowPrice))
                else:
                    curMiddleCount = curMiddleCount + 1

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
                    # statusmodifyflag = False
                    realApicalBasicFlagIndex = realApicalBasicFlagIndex + 1
                    highOrLowPrice = curUpDownData[gc.LOWPRICEKEY]
                    logging.debug("%d index date %d is basing,price(%f)" % (
                        realApicalBasicFlagIndex, tradeDateIndex, highOrLowPrice))

                # 存在更低的D
                elif lastStatus in gc.BASETYPING and highOrLowPrice > curUpDownData[gc.LOWPRICEKEY]:
                    realApicalBasicFlagList.pop(realApicalBasicFlagIndex)
                    realApicalBasicFlagList.append({tradeDateIndex: gc.BASETYPING})
                    curMiddleCount = 0
                    # statusmodifyflag = True
                    highOrLowPrice = curUpDownData[gc.LOWPRICEKEY]
                    logging.debug("%d index date %d change to lower basing,price(%f)" % (
                        realApicalBasicFlagIndex, tradeDateIndex, highOrLowPrice))
                else:
                    curMiddleCount = curMiddleCount + 1
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
        # 但是如果最后一个后续已经存在处理后5根，那么就依然成立。
        if realApicalBasicFlagIndex >= 0:
            if lastStatus in gc.BASETYPING and newlowprice > highOrLowPrice and curMiddleCount >= 4:
                curMiddleCount = 0
            elif lastStatus in gc.APICALTYPING and newhighprice < highOrLowPrice and curMiddleCount >= 4:
                curMiddleCount = 0
            else:
                logging.info(
                    "because of laststatus is %s and newprice(high(%f),low(%f)) highorlowprice(%f),curmidelecount(%d),should pop" % (
                        lastStatus, newhighprice, newlowprice, highOrLowPrice, curMiddleCount))
                realApicalBasicFlagList.pop(realApicalBasicFlagIndex)
                realApicalBasicFlagIndex = realApicalBasicFlagIndex - 1

            # print("%d这条暂时不能认为是顶或者底" % (realApicalBasicFlagIndex + 1))
        # print(realApicalBasicFlagList)
        # 根据realApicalBasicFlagList进行顶或者底的更新
        updatetblsql = sc.ENTDAYTRADEDATA_UPDATETBL % realTblName
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
                logging.error("数据库更新异常:" + updateabflagsql)
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
            srcTable = "entdaytradedata"
            realTblName = pb.getRealTableName(srcTable, self.prod_code)
            tradeDataSql = sc.ENTDAYTRADEDATA_MAXTRADEDATEGET % (realTblName, self.prod_code)
            souceDbTrade = dbcnt.getDBCntInfoByTableName(srcTable, self.prod_code)
            destRetList = souceDbTrade.execSelectSmallSql(tradeDataSql)
            maxtradedate = 0
            if len(destRetList) > 0:
                maxtradedate = destRetList[0]['maxtradedate']

            srcTable = "producttradedata"
            souceDbTrade = dbcnt.getDBCntInfoByTableName(srcTable, self.prod_code)
            tradeDataSql = sc.DAYTRADEDATA_GET % (self.prod_code, maxtradedate)

        tradeDataList = souceDbTrade.execSelectAllSql(tradeDataSql)
        # print(type(tradeDataList))
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
    进程并发，每个进程都有自己的数据库连接
    :param databaseno: productdatabaserule的logicname的trade1,trade2,trade3
    :return:
    '''
    stocklog.initLogging(logicname)
    try:
        dbCntInfo = dbcnt.createDbConnect(dbpool=False)
        productBasicInfodf = pb.getAllProductBasicInfo(dbCntInfo, ipostatus='A')
        for rowIndex in productBasicInfodf.index:
            oneProductTuple = productBasicInfodf.iloc[rowIndex]
            productCode = oneProductTuple["product_code"]  ## 产品代码
            tradelogicname = dbCntInfo.getTradeLogicNameByProductCodeAndTradeDate(productCode, 0)
            if logicname not in tradelogicname:
                continue
            # if productCode not in ("002236", "002167", '002039', '002209'):
            #     continue
            logging.info("%d productcode(%s) begin to deal" % (rowIndex, productCode))
            entangLingTheory = EntangLingTheory(productCode)
            resultret = entangLingTheory.kLineMerge(gc.K_DAY)
            if resultret is not None:
                break
            logging.info("productcode(%s) finish!" % productCode)
        logging.info("future all finished!")
    finally:
        dbCntInfo.closeAllDBConnect()
    return None


# def centraljudge(linelist, startindex, centralqj):
#     '''
#     判断linelist[startindex],linelist[startindex+2],linelist[startindex+4]三者是否存在中枢，
#     中枢区间与centralqj与相交值
#     :param linelist:
#     :param startindex:
#     :param centralqj:
#     :return:
#     '''
#     glprice = centralqj[0]
#     dhprice = centralqj[1]
#     updownflag = linelist[startindex][6]
#
#     # 要判断向下
#     if updownflag in gc.DOWNTYPING
#
#
#
#     return (glprice, dhprice)

def enttheoryfirbuy(logicname, klineType='D') -> list:
    '''
     依据传入的级别，寻找一买
     下跌过程中，至少存在一个中枢(可以是一段时间在较窄的区间震荡，一直不形成中枢)
     apicalbasiclist 这个格式是list[list],内部的list记录内容[起始日期，起始时间,价格，终止日期，终止时间, 价格，'Z/U/D',第几个中枢],
     U:上涨一笔，D下跌一笔，Z中枢中的笔,如果为Z，则第几个中枢需要输入，为1,2,3， 从1开始，如果是U或者D，则都填写为0
     由于要找的是将有机会出现一买，因此对应的特征序列是找向上的笔。向上笔有重叠区间，那么就是一个中枢

     先通过中枢来终结，再通过1+1来终结

     就花时间把一买写写好，二买也是一买后的

    :param self:
    :param klineType:
    :return:
    '''
    import copy

    firstbuyprodlist = []
    stocklog.initLogging(logicname)
    try:
        dbCntInfo = dbcnt.createDbConnect(dbpool=False)
        productBasicInfodf = pb.getAllProductBasicInfo(dbCntInfo, ipostatus='A')
        for rowIndex in productBasicInfodf.index:
            oneProductTuple = productBasicInfodf.iloc[rowIndex]
            productcode = oneProductTuple["product_code"]  ## 产品代码
            tradelogicname = dbCntInfo.getTradeLogicNameByProductCodeAndTradeDate(productcode, 0)
            if logicname not in tradelogicname:
                continue
            # if productcode not in ("002236", "002167", '002039', '002209'):
            #     continue
            logging.info("logic(%s) %d productcode(%s) begin to find first buy" % (logicname, rowIndex, productcode))

            lastyeartoday = 0
            lastyeartime = 0
            curtblname = gc.SOURCETABLEDICT[klineType]
            lastworkday = 0
            todayhighprice = 0
            todaylowprice = 0
            if klineType in gc.K_DAY:
                # 读取近一年数据，一个股票不可能一年一直再跌，如果是的话则可关注
                lastyeartoday = pb.getlastyear()
                lastworkday = pb.getlastworkday()
                # lastworkday = 20200713
                selectSql = sc.DAYTRADEDATA_ONEDATEGET % (productcode, lastworkday)
                dbtradecnt = dbcnt.getDBCntInfoByTableName(curtblname, productcode)
                entdayTrDataList = dbtradecnt.execSelectAllSql(selectSql)
                # 最近这些股票可能停牌了导致股价没有今日的
                if len(entdayTrDataList) == 0:
                    logging.debug("%d productcode(%s) do stop now? " % (lastworkday, productcode))
                    continue
                todayhighprice = float(entdayTrDataList[0][gc.HIGHPRICEKEY])
                todaylowprice = float(entdayTrDataList[0][gc.LOWPRICEKEY])
                logging.debug("%d productcode(%s),lowprice(%f)" % (
                    lastworkday, productcode, todaylowprice))

            realtablaname = pb.getRealTableName(curtblname, productcode)
            selectSql = sc.ENTDAYTRADEDATA_ABTYPINGGET % (realtablaname, productcode, lastyeartoday, lastyeartime)
            dbtradecnt = dbcnt.getDBCntInfoByTableName(curtblname, productcode)
            entdayTrDataList = dbtradecnt.execSelectAllSql(selectSql)
            if len(entdayTrDataList) == 0:
                logging.info("productcode(%s) no data be found,selectSql(%s)" % (productcode, selectSql))
                continue
            # 逆序, df中的值都是顶和底的笔表示
            entdayTrDataDf = pd.DataFrame(entdayTrDataList)
            entdayTrDataDf = entdayTrDataDf.set_index([gc.TRADEDATEKEY, gc.TRADETIMEKEY])
            for col in gc.ENTPRICE_COL:
                entdayTrDataDf[col] = entdayTrDataDf[col].astype(float)

            # 获取最高点，获取最高点右侧最低点，当前lowprice；最低点和lowprice
            # 如果lowprice比ddprice还高，那么可以不用考虑
            # print(productcode + " begin")

            # print(entdayTrDataDf[gc.HIGHPRICEKEY].max())
            # print(entdayTrDataDf[gc.HIGHPRICEKEY].idxmax(axis=0))
            maxtradeindex = entdayTrDataDf[gc.HIGHPRICEKEY].idxmax(axis=0)
            # print(maxtradeindex)
            mintradeindex = entdayTrDataDf.loc[maxtradeindex[0]:].loc[maxtradeindex[1]:][gc.LOWPRICEKEY].idxmin(axis=0)
            # 查找比索引大的日期的最小值
            # print(mintradeindex)
            # print(productcode + " end")
            if maxtradeindex[0] == mintradeindex[0] and maxtradeindex[1] == mintradeindex[1]:
                logging.info(
                    "productcode(%s) maxprice and minprice is the same!" % productcode)
                continue
            minlowprice = entdayTrDataDf.loc[mintradeindex][gc.LOWPRICEKEY]
            if todaylowprice - minlowprice > 0:
                timediff = pb.gettimediff(mintradeindex[0], mintradeindex[1], lastworkday, 0)
                if timediff > 6:
                    logging.info(
                        "productcode(%s) distince first buy to long!" % productcode)
                    continue

            curEntdayTrDataDf = entdayTrDataDf.iloc[::-1]
            # tuple (20190710, 0) Series
            firsttime = 0
            nextprodcodeflag = False
            apicalbasiclist = []
            curinnerlist = []
            for tradedatetupleIndex, curapcialbasicserialdata in curEntdayTrDataDf.iterrows():
                # print(type(tradedatetupleIndex))
                # print(tradedatetupleIndex)
                # print(type(curapcialbasicserialdata))
                # print(curapcialbasicserialdata)
                # 想要出现一买，必须首先找到的是顶分型，之后如果做出底分型才能是一买，如果先找到底分型则跳过。
                updownstatus = curapcialbasicserialdata[gc.UPDOWNFLAGKEY]
                if firsttime == 0 and updownstatus in gc.BASETYPING:
                    nextprodcodeflag = True
                    logging.info(
                        "%d productcode(%s) first type not apicaltyping!" % (tradedatetupleIndex[0], productcode))
                    break
                #
                if firsttime == 0 and updownstatus in gc.APICALTYPING:
                    if todayhighprice > curapcialbasicserialdata[gc.HIGHPRICEKEY]:
                        nextprodcodeflag = True
                        logging.info(
                            "%d productcode(%s) todayhighprice(%f) bigger apicaltyping price(%f)!" % (
                                tradedatetupleIndex[0], productcode, todayhighprice,
                                curapcialbasicserialdata[gc.HIGHPRICEKEY]))
                        break
                # 1. 出现中枢，或者平台整理, 找到一个底比之前的顶都高,图形参考下跌的图形.png，超过这个图形的再说
                # 中枢开始的顶，需要满足1.1 顶之前的底
                if updownstatus in gc.APICALTYPING:
                    firsttime = firsttime + 1
                    # 日期
                    curinnerlist.append(tradedatetupleIndex[0])
                    # 时间
                    curinnerlist.append(tradedatetupleIndex[1])
                    curinnerlist.append(curapcialbasicserialdata[gc.HIGHPRICEKEY])
                    if len(curinnerlist) >= 6:
                        curinnerlist.append(gc.DOWNTYPING)
                        curinnerlist.append(0)
                        apicalbasiclist.append(copy.deepcopy(curinnerlist))
                        curinnerlist.clear()
                        # 日期
                        curinnerlist.append(tradedatetupleIndex[0])
                        # 时间
                        curinnerlist.append(tradedatetupleIndex[1])
                        curinnerlist.append(curapcialbasicserialdata[gc.HIGHPRICEKEY])
                    # apicalbasiclist.append((updownstatus, curapcialbasicserialdata[gc.HIGHPRICEKEY]))
                    # maxapicalprice = max(maxapicalprice, curapcialbasicserialdata[gc.HIGHPRICEKEY])
                    # zcfirst = zcfirst + 1
                    # firsttime = firsttime + 1
                    logging.info("%d productcode(%s) is apicaltyping!" % (tradedatetupleIndex[0], productcode))
                elif updownstatus in gc.BASETYPING:
                    logging.info("%d productcode(%s) is basetyping!" % (tradedatetupleIndex[0], productcode))
                    # 日期
                    curinnerlist.append(tradedatetupleIndex[0])
                    # 时间
                    curinnerlist.append(tradedatetupleIndex[1])
                    curinnerlist.append(curapcialbasicserialdata[gc.LOWPRICEKEY])
                    if len(curinnerlist) >= 6:
                        curinnerlist.append(gc.UPTYPING)
                        curinnerlist.append(0)
                        apicalbasiclist.append(copy.deepcopy(curinnerlist))
                        curinnerlist.clear()
                        # 日期
                        curinnerlist.append(tradedatetupleIndex[0])
                        # 时间
                        curinnerlist.append(tradedatetupleIndex[1])
                        curinnerlist.append(curapcialbasicserialdata[gc.LOWPRICEKEY])
            logging.info("productcode(%s) bi merge finish!" % productcode)
            # print(apicalbasiclist)
            # 由于要找的是将有机会出现一买，因此对应的特征序列是找向上的笔。向上笔有重叠区间，那么就是一个中枢
            zcgdpricelist = []
            ggprice = gc.MINPRICE
            glprice = gc.MAXPRICE
            ddprice = gc.MAXPRICE
            dlprice = gc.MINPRICE
            firsttime = 0
            zsstartdate = 0
            zsstarttime = 0
            zsenddate = 0
            zsendtime = 0
            lastddprice = 0
            # 记录第一次脱离中枢的位置
            # 中枢实际上有4段重叠的区域，进入笔，然后是上下上三笔，此四笔是存在重叠区域。
            # 现在如果是通过特征序列进行判断， 特征序列的笔是来判断是否中枢截止了。
            # 进入下笔和下、下的三笔决定了这段区间一定存在中枢
            curendzsindex = 0
            centralqj = (9999999.99, 0)
            for curlistindex in range(len(apicalbasiclist)):
                curinnerlist = apicalbasiclist[curlistindex]
                if curinnerlist[6] in gc.DOWNTYPING:
                    continue

                if firsttime == 0:
                    ggprice = curinnerlist[2]
                    glprice = curinnerlist[2]
                    ddprice = curinnerlist[5]
                    dlprice = curinnerlist[5]
                    firsttime = firsttime + 1
                    zsstartdate = curinnerlist[0]
                    zsstarttime = curinnerlist[1]
                else:
                    # 形成中枢了。
                    if curinnerlist[5] < glprice:
                        ggprice = max(ggprice, curinnerlist[2])
                        glprice = min(glprice, curinnerlist[2])
                        ddprice = min(ddprice, curinnerlist[5])
                        dlprice = max(dlprice, curinnerlist[5])
                        zsenddate = curinnerlist[3]
                        zsendtime = curinnerlist[4]
                    else:
                        # 存在某一笔在中枢下方，不合理，已经结束
                        if curinnerlist[2] < dlprice:
                            nextprodcodeflag = True
                            break
                        if ggprice != gc.MAXPRICE:
                            zcgdpricelist.append([zsenddate, zsendtime, zsstartdate, zsstarttime, dlprice, glprice])
                            # 此时需要判断是否1+1终结,这个时候需要判断是向下的两笔是否满足1+1终结的条件, 这里不能这么简单的判断，
                            # 因为如果是多个中枢的情况就没办法判断了。
                            # curendzsindex = curlistindex
                            afterlistindex = curlistindex - 1
                            beforelistindex = curlistindex + 1
                            befbeforelistindex = beforelistindex + 2
                            if befbeforelistindex < len(apicalbasiclist):
                                befbeforedatalist = apicalbasiclist[befbeforelistindex]
                                beforedatalist = apicalbasiclist[beforelistindex]
                                afterdatalist = apicalbasiclist[afterlistindex]
                                if befbeforedatalist[2] < beforedatalist[2] and beforedatalist[2] > afterdatalist[2] and \
                                        beforedatalist[5] > afterdatalist[5]:
                                    nextprodcodeflag = True
                                    logging.info(
                                        "date(%d,%d)productcode(%s)  1+1 three k end, the highest price(%f)!" % (
                                            beforedatalist[3], beforedatalist[4], productcode, beforedatalist[5]))
                                    break
                            elif beforelistindex < len(apicalbasiclist):
                                beforedatalist = apicalbasiclist[beforelistindex]
                                afterdatalist = apicalbasiclist[afterlistindex]
                                # 1 + 1终结
                                if beforedatalist[2] > afterdatalist[2] and beforedatalist[5] > afterdatalist[5]:
                                    nextprodcodeflag = True
                                    logging.info(
                                        "date(%d,%d)productcode(%s)  1+1 two k end, the highest price(%f)!" % (
                                            beforedatalist[3], beforedatalist[4], productcode, beforedatalist[5]))
                                    break

                        firsttime = 0
                        ggprice = curinnerlist[2]
                        glprice = curinnerlist[2]
                        ddprice = curinnerlist[5]
                        dlprice = curinnerlist[5]
                        firsttime = firsttime + 1
                        zsstartdate = curinnerlist[0]
                        zsstarttime = curinnerlist[1]
            if nextprodcodeflag is True:
                if len(zcgdpricelist) == 0:
                    logging.info("productcode(%s) first type not apicaltyping!" % productcode)
                    continue
                else:
                    firstbuyprodlist.append(productcode)
                    logging.info("productcode(%s) be found exist first buy!" % productcode)
                    print("productcode(%s) begin to found exist first buy!" % productcode)
                    print(zcgdpricelist)
                    print("productcode(%s) end to found exist first buy!" % productcode)

            logging.info("productcode(%s) finish finding first buy!" % productcode)
        print("future all finished!")
    finally:
        logging.info(logicname + " close all dbconnect!")
        dbCntInfo.closeAllDBConnect()
    return firstbuyprodlist


# def enttheorysecbuy(logicname, klineType=gc.K_DAY) -> list:
#     '''
#      依据传入的级别，寻找二买
#      1. 已经出现一买
#
#      下跌过程中，至少存在一个中枢(可以是一段时间在较窄的区间震荡，一直不形成中枢)
#      apicalbasiclist 这个格式是list[list],内部的list记录内容[起始日期，起始时间,价格，终止日期，终止时间, 价格，'Z/U/D',第几个中枢],
#      U:上涨一笔，D下跌一笔，Z中枢中的笔,如果为Z，则第几个中枢需要输入，为1,2,3， 从1开始，如果是U或者D，则都填写为0
#      由于要找的是将有机会出现一买，因此对应的特征序列是找向上的笔。向上笔有重叠区间，那么就是一个中枢
#
#      先通过中枢来终结，再通过1+1来终结
#
#     :param self:
#     :param klineType:
#     :return:
#     '''
#     import copy
#
#     secbuyprodlist = []
#     stocklog.initLogging(logicname)
#     try:
#         dbCntInfo = dbcnt.createDbConnect(dbpool=False)
#         productBasicInfodf = pb.getAllProductBasicInfo(dbCntInfo, ipostatus='A')
#         for rowIndex in productBasicInfodf.index:
#             oneProductTuple = productBasicInfodf.iloc[rowIndex]
#             productcode = oneProductTuple["product_code"]  ## 产品代码
#             tradelogicname = dbCntInfo.getTradeLogicNameByProductCodeAndTradeDate(productcode, 0)
#             if logicname not in tradelogicname:
#                 continue
#             # if productcode not in ("002236", "002167", '002039', '002209'):
#             #     continue
#             logging.info("logic(%s) %d productcode(%s) begin to find second buy" % (logicname, rowIndex, productcode))
#
#             lastyeartoday = 0
#             lastyeartime = 0
#             curtblname = gc.SOURCETABLEDICT[klineType]
#             lastworkday = 0
#             todayhighprice = 0
#             todaylowprice = 0
#             if klineType in gc.K_DAY:
#                 # 读取近一年数据，一个股票不可能一年一直再跌，如果是的话则可关注
#                 lastyeartoday = pb.getlastyear()
#                 lastworkday = pb.getlastworkday()
#                 # lastworkday = 20200713
#                 selectSql = sc.DAYTRADEDATA_ONEDATEGET % (productcode, lastworkday)
#                 dbtradecnt = dbcnt.getDBCntInfoByTableName(curtblname, productcode)
#                 entdayTrDataList = dbtradecnt.execSelectAllSql(selectSql)
#                 # 最近这些股票可能停牌了导致股价没有今日的
#                 if len(entdayTrDataList) == 0:
#                     logging.debug("%d productcode(%s) do stop now! " % (lastworkday, productcode))
#                     continue
#                 todayhighprice = float(entdayTrDataList[0][gc.HIGHPRICEKEY])
#                 todaylowprice = float(entdayTrDataList[0][gc.LOWPRICEKEY])
#                 logging.debug("%d productcode(%s),lowprice(%f)" % (
#                     lastworkday, productcode, todaylowprice))
#
#             realtablaname = pb.getRealTableName(curtblname, productcode)
#             selectSql = sc.ENTDAYTRADEDATA_ABTYPINGGET % (realtablaname, productcode, lastyeartoday, lastyeartime)
#             dbtradecnt = dbcnt.getDBCntInfoByTableName(curtblname, productcode)
#             entdayTrDataList = dbtradecnt.execSelectAllSql(selectSql)
#             if len(entdayTrDataList) == 0:
#                 logging.info("productcode(%s) no data be found,selectSql(%s)" % (productcode, selectSql))
#                 continue
#             # 逆序, df中的值都是顶和底的笔表示
#             entdayTrDataDf = pd.DataFrame(entdayTrDataList)
#             entdayTrDataDf = entdayTrDataDf.set_index([gc.TRADEDATEKEY, gc.TRADETIMEKEY])
#             for col in gc.ENTPRICE_COL:
#                 entdayTrDataDf[col] = entdayTrDataDf[col].astype(float)
#
#             # 获取最高点，获取最高点右侧最低点，当前lowprice；最低点和lowprice
#             # 如果lowprice比ddprice还高，那么可以不用考虑
#             maxtradeindex = entdayTrDataDf[gc.HIGHPRICEKEY].idxmax(axis=0)
#             # print(maxtradeindex)
#             mintradeindex = entdayTrDataDf.loc[maxtradeindex[0]:].loc[maxtradeindex[1]:][gc.LOWPRICEKEY].idxmin(axis=0)
#             # 查找比索引大的日期的最小值
#             # print(mintradeindex)
#             # print(productcode + " end")
#             logging.debug(
#                 "productcode(%s) from maxdate(%d),maxtime(%d) to mindate(%d), mintime(%d)  maxprice and minprice is the same!" % (
#                     productcode, maxtradeindex[0], maxtradeindex[1], mintradeindex[0], mintradeindex[1]))
#             if maxtradeindex[0] == mintradeindex[0] and maxtradeindex[1] == mintradeindex[1]:
#                 logging.info(
#                     "productcode(%s) maxprice and minprice is the same!" % productcode)
#                 continue
#             minlowprice = entdayTrDataDf.loc[mintradeindex][gc.LOWPRICEKEY]
#             if todaylowprice < minlowprice:
#                 logging.info(
#                     "productcode(%s) todayprice(%f) bigger than minlowprice(%f)!" % (
#                     productcode, todaylowprice, minlowprice))
#                 continue
#
#             curEntdayTrDataDf = entdayTrDataDf.iloc[::-1]
#             # tuple (20190710, 0) Series
#             firsttime = 0
#             nextprodcodeflag = False
#             apicalbasiclist = []
#             curinnerlist = []
#             for tradedatetupleIndex, curapcialbasicserialdata in curEntdayTrDataDf.iterrows():
#                 # 想要出现二买，必须首先找到的是顶分型，之后如果做出底分型才能是二买，如果先找到底分型则跳过。
#                 updownstatus = curapcialbasicserialdata[gc.UPDOWNFLAGKEY]
#                 if firsttime == 0 and updownstatus in gc.BASETYPING:
#                     nextprodcodeflag = True
#                     logging.info(
#                         "%d productcode(%s) second type not apicaltyping!" % (tradedatetupleIndex[0], productcode))
#                     break
#                 # 顶分型还未结束，一般不会出现这种误判
#                 if firsttime == 0 and updownstatus in gc.APICALTYPING:
#                     if todayhighprice > curapcialbasicserialdata[gc.HIGHPRICEKEY]:
#                         nextprodcodeflag = True
#                         logging.info(
#                             "%d productcode(%s) todayhighprice(%f) bigger apicaltyping price(%f)!" % (
#                                 tradedatetupleIndex[0], productcode, todayhighprice,
#                                 curapcialbasicserialdata[gc.HIGHPRICEKEY]))
#                         break
#                 # 1. 出现中枢，或者平台整理, 找到一个底比之前的顶都高,图形参考下跌的图形.png，超过这个图形的再说
#                 # 中枢开始的顶，需要满足1.1 顶之前的底
#                 if updownstatus in gc.APICALTYPING:
#                     firsttime = firsttime + 1
#                     # 日期
#                     curinnerlist.append(tradedatetupleIndex[0])
#                     # 时间
#                     curinnerlist.append(tradedatetupleIndex[1])
#                     curinnerlist.append(curapcialbasicserialdata[gc.HIGHPRICEKEY])
#                     if len(curinnerlist) >= 6:
#                         curinnerlist.append(gc.DOWNTYPING)
#                         curinnerlist.append(0)
#                         apicalbasiclist.append(copy.deepcopy(curinnerlist))
#                         curinnerlist.clear()
#                         # 日期
#                         curinnerlist.append(tradedatetupleIndex[0])
#                         # 时间
#                         curinnerlist.append(tradedatetupleIndex[1])
#                         curinnerlist.append(curapcialbasicserialdata[gc.HIGHPRICEKEY])
#                     # apicalbasiclist.append((updownstatus, curapcialbasicserialdata[gc.HIGHPRICEKEY]))
#                     # maxapicalprice = max(maxapicalprice, curapcialbasicserialdata[gc.HIGHPRICEKEY])
#                     # zcfirst = zcfirst + 1
#                     # firsttime = firsttime + 1
#                     logging.info("%d productcode(%s) is apicaltyping!" % (tradedatetupleIndex[0], productcode))
#                 elif updownstatus in gc.BASETYPING:
#                     logging.info("%d productcode(%s) is basetyping!" % (tradedatetupleIndex[0], productcode))
#                     # 日期
#                     curinnerlist.append(tradedatetupleIndex[0])
#                     # 时间
#                     curinnerlist.append(tradedatetupleIndex[1])
#                     curinnerlist.append(curapcialbasicserialdata[gc.LOWPRICEKEY])
#                     if len(curinnerlist) >= 6:
#                         curinnerlist.append(gc.UPTYPING)
#                         curinnerlist.append(0)
#                         apicalbasiclist.append(copy.deepcopy(curinnerlist))
#                         curinnerlist.clear()
#                         # 日期
#                         curinnerlist.append(tradedatetupleIndex[0])
#                         # 时间
#                         curinnerlist.append(tradedatetupleIndex[1])
#                         curinnerlist.append(curapcialbasicserialdata[gc.LOWPRICEKEY])
#             logging.info("productcode(%s) bi merge finish!" % productcode)
#             # print(apicalbasiclist)
#             # 由于要找的是将有机会出现二买，因此对应的特征序列是找向上的笔。向上笔有重叠区间，那么就是一个中枢
#             zcgdpricelist = []
#             ggprice = gc.MINPRICE
#             glprice = gc.MAXPRICE
#             ddprice = gc.MAXPRICE
#             dlprice = gc.MINPRICE
#             firsttime = 0
#             zsstartdate = 0
#             zsstarttime = 0
#             zsenddate = 0
#             zsendtime = 0
#             lastddprice = 0
#             # 记录第一次脱离中枢的位置
#             # 中枢实际上有4段重叠的区域，进入笔，然后是上下上三笔，此四笔是存在重叠区域。
#             # 现在如果是通过特征序列进行判断， 特征序列的笔是来判断是否中枢截止了。
#             # 进入下笔和下、下的三笔决定了这段区间一定存在中枢
#             curendzsindex = 0
#             for curlistindex in range(len(apicalbasiclist)):
#                 curinnerlist = apicalbasiclist[curlistindex]
#                 if curinnerlist[6] not in gc.UPTYPING:
#                     continue
#
#                 if firsttime == 0:
#                     ggprice = curinnerlist[2]
#                     glprice = curinnerlist[2]
#                     ddprice = curinnerlist[5]
#                     dlprice = curinnerlist[5]
#                     firsttime = firsttime + 1
#                     zsstartdate = curinnerlist[0]
#                     zsstarttime = curinnerlist[1]
#                 else:
#                     if curinnerlist[5] < glprice:
#                         # 一买后的反弹有进入中枢的可能，比较强势；没进入中枢的场景就直接pass，反弹弱就是形成3卖了。
#                         if firsttime == 1:
#                             ggprice = curinnerlist[2]
#                             glprice = curinnerlist[2]
#                             ddprice = curinnerlist[5]
#                             dlprice = curinnerlist[5]
#                             firsttime = firsttime + 1
#                             zsstartdate = curinnerlist[0]
#                             zsstarttime = curinnerlist[1]
#                         else:
#                             firsttime = firsttime + 1
#                             ggprice = max(ggprice, curinnerlist[2])
#                             glprice = min(glprice, curinnerlist[2])
#                             ddprice = min(ddprice, curinnerlist[5])
#                             dlprice = max(dlprice, curinnerlist[5])
#                             zsenddate = curinnerlist[3]
#                             zsendtime = curinnerlist[4]
#                     else:
#                         # 存在某一笔在中枢下方，不合理，已经结束
#                         if curinnerlist[2] < dlprice:
#                             nextprodcodeflag = True
#                             break
#                         if ggprice != gc.MAXPRICE:
#                             zcgdpricelist.append([zsenddate, zsendtime, zsstartdate, zsstarttime, dlprice, glprice])
#                             # 此时需要判断是否1+1终结,这个时候需要判断是向下的两笔是否满足1+1终结的条件, 这里不能这么简单的判断，
#                             # 因为如果是多个中枢的情况就没办法判断了。
#                             # curendzsindex = curlistindex
#                             afterlistindex = curlistindex - 1
#                             beforelistindex = curlistindex + 1
#                             befbeforelistindex = beforelistindex + 2
#                             if befbeforelistindex < len(apicalbasiclist):
#                                 befbeforedatalist = apicalbasiclist[befbeforelistindex]
#                                 beforedatalist = apicalbasiclist[beforelistindex]
#                                 afterdatalist = apicalbasiclist[afterlistindex]
#                                 if befbeforedatalist[2] < beforedatalist[2] and beforedatalist[2] > afterdatalist[2] and \
#                                         beforedatalist[5] > afterdatalist[5]:
#                                     nextprodcodeflag = True
#                                     logging.info(
#                                         "date(%d,%d)productcode(%s)  1+1 three k end, the highest price(%f)!" % (
#                                             beforedatalist[3], beforedatalist[4], productcode, beforedatalist[5]))
#                                     break
#                             elif beforelistindex < len(apicalbasiclist):
#                                 beforedatalist = apicalbasiclist[beforelistindex]
#                                 afterdatalist = apicalbasiclist[afterlistindex]
#                                 # 1 + 1终结
#                                 if beforedatalist[2] > afterdatalist[2] and beforedatalist[5] > afterdatalist[5]:
#                                     nextprodcodeflag = True
#                                     logging.info(
#                                         "date(%d,%d)productcode(%s)  1+1 two k end, the highest price(%f)!" % (
#                                             beforedatalist[3], beforedatalist[4], productcode, beforedatalist[5]))
#                                     break
#
#                         firsttime = 0
#                         ggprice = curinnerlist[2]
#                         glprice = curinnerlist[2]
#                         ddprice = curinnerlist[5]
#                         dlprice = curinnerlist[5]
#                         firsttime = firsttime + 1
#                         zsstartdate = curinnerlist[0]
#                         zsstarttime = curinnerlist[1]
#             if nextprodcodeflag is True:
#                 if len(zcgdpricelist) == 0:
#                     logging.info("productcode(%s) first type not apicaltyping!" % productcode)
#                     continue
#                 else:
#                     secbuyprodlist.append(productcode)
#                     logging.info("productcode(%s) be found exist first buy!" % productcode)
#                     print("productcode(%s) begin to found exist first buy!" % productcode)
#                     print(zcgdpricelist)
#                     print("productcode(%s) end to found exist first buy!" % productcode)
#
#             logging.info("productcode(%s) finish finding first buy!" % productcode)
#         print("future all finished!")
#     finally:
#         logging.info(logicname + " close all dbconnect!")
#         dbCntInfo.closeAllDBConnect()
#
#     return secbuyprodlist
#
#
# def enttheorythirdbuy(logicname, klineType='D') -> list:
#     '''
#      依据传入的级别，寻找三买
#     :param self:
#     :param klineType:
#     :return: 符合条件的产品列表
#     '''
#
#     thirbuyprodlist = []
#     return thirbuyprodlist
#
#
# def enttheoryincentral(logicname, klineType='D') -> list:
#     '''
#      依据传入的级别，产品在中枢中
#     :param self:
#     :param klineType:
#     :return: 符合条件的产品列表
#     '''
#
#     centralprodlist = []
#     return centralprodlist
#
#
# def enttheoryfirstsell(logicname, klineType='D') -> list:
#     '''
#      依据传入的级别，产品在快出现一卖
#     :param self:
#     :param klineType:
#     :return: 符合条件的产品列表
#     '''
#
#     firstsellprodlist = []
#     return firstsellprodlist
#
#
# def enttheorysecondsell(logicname, klineType='D') -> list:
#     '''
#      依据传入的级别，产品在快出现二卖
#     :param self:
#     :param klineType:
#     :return: 符合条件的产品列表
#     '''
#
#     secondsellprodlist = []
#     return secondsellprodlist


from multiprocessing import Pool
from finance.servicelib.public import public as pb

if __name__ == "__main__":
    path = 'D:/software/new_haitong'

    # 按分库进行并发
    with Pool(len(gc.DBTRADELOGNAMELIST)) as p:
        print(p.map(futureKLine, gc.DBTRADELOGNAMELIST))

    # with Pool(len(gc.DBTRADELOGNAMELIST)) as p:
    #     print(p.map(enttheoryfirbuy, gc.DBTRADELOGNAMELIST))
    # futureKLine(gc.DBTRADELOGNAMELIST[3])
    # firstbuyprodlist = enttheoryfirbuy(gc.DBTRADELOGNAMELIST[3])
    # print(firstbuyprodlist)
