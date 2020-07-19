# -*- coding:utf-8 -*-
'''
 stock模块的test
'''


if __name__ == "__main__":
    import os
    import time

    import tushare as ts
    import logging
    import csv

    from finance.servicelib.processinit import dbcnt
    from finance.servicelib.processinit import stocklog
    from finance.util import SqlCons as sqlcons
    from finance.servicelib.public import public as pb

    stocklog.initLogging()
    dbCntInfo = dbcnt.createDbConnect(dbpool=False)
    df = ts.get_stock_basics()
    codelist = list(df.index)
    filename = 'G:\\nfx\\stockproj\\stockmarket\\finance\\resource\\trade30'
    for oneindex in range(len(codelist)):
        print(codelist[oneindex] + " begin")
        productCode = codelist[oneindex]
        realfilename = filename + "\\" + productCode + ".csv"
        if os.path.exists(realfilename) is not True:
            logging.info("product(%s) there is no file!"%productCode)
            continue
        logging.info("file(%s) begin to read!" % realfilename)
        sourcetable = "prod30tradedata"
        tableDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=sourcetable, productcode=productCode)
        firstline = 0
        execlSql = sqlcons.CSV30DATAINSERTDB
        with open(realfilename, 'r') as fname:
            reader = csv.reader(fname)
            print(reader)
            for row in reader:
                if firstline == 0:
                    firstline = firstline + 1
                    continue
                # print(row)
                # print(type(row[0]))
                tradedate = int(row[0][:4]+row[0][5:7]+row[0][8:10])
                tradetime = int(row[0][11:13]+row[0][14:16]+row[0][17:19])
                openPrice = float(row[1])
                highPrice = float(row[2])
                closePrice = float(row[3])
                lowPrice = float(row[4])
                productVolumn = float(row[5])
                productAmount = 0.0
                print(tradedate)
                print(tradetime)
                   # prod30tradedata(product_code, symbol_code, trade_date, trade_time, open_price, high_price,
                   #                 close_price, low_price, product_volume, product_amount)
                symbol_code = pb.code_to_symbol(productCode)
                # print(openPrice)
                # print(highPrice)
                # print(closePrice)
                # print(lowPrice)
                # print(productVolumn)
                # print(symbol_code)
                execlSql = execlSql + sqlcons.CSV30INSERTVAR % (
                    productCode, symbol_code, tradedate,tradetime, openPrice, highPrice, closePrice, lowPrice, productVolumn, productAmount)
                firstline = firstline + 1
                if firstline == 100:
                    excepte = tableDbBase.execNotSelectSql(execlSql[:-1])
                    if excepte is not None:
                        print(excepte)
                        print("执行异常，程序终止!")
                        break
                    execlSql = sqlcons.CSV30DATAINSERTDB
                    firstline = 1
            if len(execlSql) > len(sqlcons.CSV30DATAINSERTDB):
                excepte = tableDbBase.execNotSelectSql(execlSql[:-1])
                if excepte is not None:
                    print(excepte)
                    print("执行异常，程序终止!")
                    break

        logging.info("file(%s) read end!" % realfilename)
    dbCntInfo.closeAllDBConnect()
