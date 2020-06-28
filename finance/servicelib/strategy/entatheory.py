# -*- coding:utf-8 -*-
'''
   缠论的具体实现
'''

from finance.servicelib.public import public as pb
from finance.servicelib.processinit import dbcnt
from finance.util import SqlCons as sc
from finance.util import GlobalCons as gc
import pandas as pd


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
        resultIncTradeDataList = []
        firstTradeDataFlag = True
        trendUpOrDown = gc.TRENDFLAG_UP

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

            else:  # 无包含关系
                if gc.MERGEFLAGKKEY not in lastTradeData:
                    lastTradeData[gc.MERGEFLAGKKEY] = '0'
                resultIncTradeDataList.append(lastTradeData)
                # lastTradeData数据插入到数据库中的entdaytradedata表中
                srcTable = "entdaytradedata"
                realTblName = pb.getRealTableName(srcTable, self.prod_code)
                dbCntInfo = dbcnt.getDBCntInfoByTableName(srcTable, self.prod_code)
                # product_code, trade_date,open_price,high_price,close_price,low_price,merge_flag,updown_flag
                insertSql = sc.ENTDAYTRADEDATA_INSERT % (
                    realTblName, self.prod_code, lastTradeData[gc.TRADEDATEKEY], lastTradeData[gc.OPENPRICEKEY],
                    lastTradeData[gc.HIGHPRICEKEY], lastTradeData[gc.CLOSEPRICEKEY],
                    lastTradeData[gc.LOWPRICEKEY], lastTradeData[gc.MERGEFLAGKKEY],
                    "N")

                insertResult = dbCntInfo.execNotSelectSql(insertSql)
                if insertResult is not None:
                    print("异常语句:" + insertSql)
                    raise Exception("数据库插入异常!")  # 异常被抛出，print函数无法执行

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

        return (None,pd.DataFrame(resultIncTradeDataList))

    def kLineMerge(self, klineType='D'):
        '''
         k线做合并，就是处理前后的包含关系
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
        (incResult, incRolDf) = self.inclusionrRelotionDeal(tradeDataList)
        if incResult is not None:
            return incResult
        # 顶底分型判断


if __name__ == "__main__":
    path = 'D:/software/new_haitong'
    xmlfile = "G:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    dbCntInfo = dbcnt.createDbConnect(xmlfile, dbpool=True)
    try:
        entangLingTheory = EntangLingTheory('000001')
        entangLingTheory.kLineMerge(gc.K_DAY)
    finally:
        dbCntInfo.closeAllDBConnect()
