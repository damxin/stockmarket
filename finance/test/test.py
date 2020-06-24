# import tushare as ts
# from sqlalchemy import create_engine
# from selenium import webdriver  # 导入Selenium的webdriver
# from selenium.webdriver.common.keys import Keys  # 导入Keys
# import pymysql
# import win32gui as win32gui
from finance.servicelib.processinit import dbcnt
from pyecharts import options as opts
from pyecharts.charts import Kline
from finance.servicelib.public import public as pb


def kline_base(data):

    c = (
        Kline()
        .add_xaxis(["2017/7/{}".format(i + 1) for i in range(31)])
        .add_yaxis("kline", data)
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_scale=True),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            title_opts=opts.TitleOpts(title="Kline-基本示例"),
        )
    )
    return c

def kline_datazoom_inside(data):
    c = (
        Kline()
        .add_xaxis(["2017/7/{}".format(i + 1) for i in range(31)])
        .add_yaxis("kline", data)
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            title_opts=opts.TitleOpts(title="Kline-DataZoom-inside"),
        )
    )
    return c

# def loginichat():
#     '''
#     该功能已经失效
#     :return:
#     '''
#     import itchat as wxchat
#     wxchat.login()
#     # wxchat.send('hello filehelper', toUserName='filehelper')

# def setText(aString):
#     w.OpenClipboard()
#     w.EmptyClipboard()
#     w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
#     w.CloseClipboard()
#
#
# def setImage(data):  # 写入剪切板
#     import win32clipboard as w
#     w.OpenClipboard()
#     try:
#         # Unicode tests
#         w.EmptyClipboard()
#         w.SetClipboardData(win32con.CF_DIB, data)
#     except:
#         traceback.print_exc()
#     finally:
#         w.CloseClipboard()
# def ctrlV():
#     win32api.keybd_event(17,0,0,0)  #ctrl键位码是17
#     win32api.keybd_event(86,0,0,0)  #v键位码是86
#     win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0) #释放按键
#     win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
#
# def altS():
#     win32api.keybd_event(18, 0, 0, 0)    #Alt
#     win32api.keybd_event(83,0,0,0) #s
#     win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0) #释放按键
#     win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)

def stock_csv(softpath, filepath, name):
    import os
    import struct
    import datetime

    data = []
    with open(filepath, 'rb') as f:
        file_object_path = softpath+ '/vipdoc/sh/pythondata/' + name +'.csv'
        file_object = open(file_object_path, 'w+')
        while True:
            stock_date = f.read(4)
            stock_open = f.read(4)
            stock_high = f.read(4)
            stock_low= f.read(4)
            stock_close = f.read(4)
            stock_amount = f.read(4)
            stock_vol = f.read(4)
            stock_reservation = f.read(4)

            # date,open,high,low,close,amount,vol,reservation

            if not stock_date:
                break
            stock_date = struct.unpack("l", stock_date)     # 4字节 如20091229
            stock_open = struct.unpack("l", stock_open)     #开盘价*100
            stock_high = struct.unpack("l", stock_high)     #最高价*100
            stock_low= struct.unpack("l", stock_low)        #最低价*100
            stock_close = struct.unpack("l", stock_close)   #收盘价*100
            stock_amount = struct.unpack("f", stock_amount) #成交额
            stock_vol = struct.unpack("l", stock_vol)       #成交量
            stock_reservation = struct.unpack("l", stock_reservation) #保留值

            date_format = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d') #格式化日期
            list= date_format.strftime('%Y-%M-%d')+","+str(stock_open[0]/100)+","+str(stock_high[0]/100.0)+","+str(stock_low[0]/100.0)+","+str(stock_close[0]/100.0)+","+str(stock_vol[0])+"\r\n"
            file_object.writelines(list)
        file_object.close()

def tdxShLdayToStock(softPath,dbCntInfo, dataType="sh", relativePath=None):
    '''
    tdx数据读取到数据库中
    参考网站:https://www.jianshu.com/p/9dd3ef74fe96
    tdx目录结构：https://www.cnblogs.com/ftrako/p/3800687.html
    :param softpath:
    :param dataType:
    :return:
    '''

    import os
    import struct
    from finance.util import DictCons as dictcons
    from finance.util import SqlCons as sqlcons

    relativePath = "/vipdoc/"+dataType+"/lday/" if relativePath is None else relativePath
    absolutePath = softPath+relativePath

    sourcetable = "producttradedata"
    listTradeFile = os.listdir(absolutePath)
    for productTradeFile in listTradeFile:
        print("正在处理产品代码为的文件:" + productTradeFile)
        productCode = productTradeFile[2:-4]
        # SELECT subleft3 FROM (SELECT  LEFT(a.`product_code`,3) subleft3,a.product_code FROM producttradedata a GROUP BY a.product_code) a GROUP BY subleft3;
        # 000,001,002,003,300,600,601,603,688
        subleft3 = productCode[:3]
        marketType=""
        if subleft3 in dictcons.DICTCONS_CODETOMARKETTYPE:
            marketType = dictcons.DICTCONS_CODETOMARKETTYPE[subleft3]
            print("正在处理产品代码为(" + productCode + ")的markettype:" + str(marketType))
        else :
            print("正在处理产品代码为(" + productCode + ")的文件:" + subleft3)
            continue
        # sh000001是上证指数，而000001是平安银行是深圳A股，因此这里要过滤
        if dataType == "sz":
            if (marketType==2 or marketType == 4 or marketType == 3) is False:
                continue
        else :
            if (marketType == 1 or marketType == 8) is False:
                continue

        filepath = absolutePath + productTradeFile

        # 获取该股票的最大日期
        maxTradeDate = pb.getMaxTradeDateFromCurProductCode(dbCntInfo, productCode)
        if maxTradeDate == 190000101:
            print("当前产品%s没有在productbaseinfo表中,请添加!"%productCode)
        print("正在处理产品代码为(" + productCode + ")的文件:" + filepath+"("+str(maxTradeDate)+")")
        tableDbBase = dbCntInfo.getDBCntInfoByTableName(tablename=sourcetable, productcode=productCode)
        with open(filepath, 'rb') as fname:
            while True:
                stock_date = fname.read(4)
                stock_open = fname.read(4)
                stock_high = fname.read(4)
                stock_low = fname.read(4)
                stock_close = fname.read(4)
                stock_amount = fname.read(4)
                stock_vol = fname.read(4)
                stock_reservation = fname.read(4)

                # date,open,high,low,close,amount,vol,reservation

                if not stock_date:
                    break
                stock_date = struct.unpack("l", stock_date)  # 4字节 如20091229

                tradedate = stock_date[0]
                if tradedate<=maxTradeDate:
                    continue
                stock_open = struct.unpack("l", stock_open)  # 开盘价*100
                openPrice = stock_open[0]/100.0
                stock_high = struct.unpack("l", stock_high)  # 最高价*100
                highPrice = stock_high[0]/100.0
                stock_low = struct.unpack("l", stock_low)  # 最低价*100
                lowPrice = stock_low[0]/100.0
                stock_close = struct.unpack("l", stock_close)  # 收盘价*100
                closePrice = stock_close[0] / 100.0
                stock_amount = struct.unpack("f", stock_amount)  # 成交额
                productAmount = stock_amount[0]
                stock_vol = struct.unpack("l", stock_vol)  # 成交量
                productVolumn = stock_vol[0]
                # stock_reservation = struct.unpack("l", stock_reservation)  # 保留值
                # print("%d,%f"%(tradedate,openPrice))
                # 数据插入到数据库中
                # product_code, trade_date,open_price,high_price,close_price,low_price,product_volume,product_amount
                execlSql = sqlcons.TDXDATAINSERTDATABASE%(productCode,tradedate,openPrice,highPrice,closePrice,lowPrice,productVolumn,productAmount)
                excepte = tableDbBase.execNotSelectSql(execlSql)
                if excepte is not None :
                    print(excepte)
                    print("productVolumn(%f),productAmount(%f)"%(productVolumn,productAmount))
                    print("执行异常，程序终止!")
                    return excepte
        print("产品代码为(" + productCode + ")的文件处理完毕!")
    return None

if __name__ == "__main__":
    path = 'D:/software/new_haitong'
    xmlfile = "G:\\nfx\\Python\\stockmarket\\finance\\resource\\finance.xml"
    dbCntInfo = dbcnt.DbCnt(xmlfile)
    resultexpt = tdxShLdayToStock(path,dbCntInfo,"sz")
    if resultexpt is None:
        tdxShLdayToStock(path, dbCntInfo, "sh")
    dbCntInfo.closeAllDBConnect()
    # return
# loginichat()
# import sys;sys.argv = ['', 'Test.testName']
# df = ts.get_hist_data("000001", start='2019-08-22', end='2019-08-31')
# print(df)
# df = ts.get_stock_basics()
# engine = create_engine('mysql+pymysql://root:root@127.0.0.1/stockmarket?charset=utf8')
# df.to_sql('stock_basics', engine, if_exists="replace", index=False)
# print("finish")
# print(df)
# driver = webdriver.Chrome()  # 指定使用的浏览器，初始化webdriver
# driver.get("http://www.python.org")  # 请求网页地址
# assert "Python" in driver.title  # 看看Python关键字是否在网页title中，如果在则继续，如果不在，程序跳出。
# elem = driver.find_element_by_name("q")  # 找到name为q的元素，这里是个搜索框
# elem.clear()  # 清空搜索框中的内容
# elem.send_keys("pycon")  # 在搜索框中输入pycon
# elem.send_keys(Keys.RETURN)  # 相当于回车键，提交
# assert "No results found." not in driver.page_source  # 如果当前页面文本中有“No results found.”则程序跳出
# driver.close()  # 关闭webdriver

#
# #1.创建与数据库连接对象
# db =pymysql.connect(host="127.0.0.1",user="root",
#                    password="root",database="db4",
#                    charset="utf8")
#
# #2.利用db方法创建游标对象
# cur = db.cursor()
#
# #3.利用游标对象execute()方法执行SQL命令
# #cur.execute(";") #这里填写正确的SQL语句  例如:
# cur.execute("insert into sheng values\
#             (16,300000,'台湾省');")
# #4.提交到数据库执行
# db.commit()
# print("OK")
# #5.关闭游标对象
# cur.close()
#
# #6.断开数据库连接
# db.close()
#     data = [
#         [3000, 1000, 4000, 5000], #        high
#         [2300, 2291.3, 2288.26, 2308.38],
#         [2295.35, 2346.5, 2295.35, 2345.92],
#         [2347.22, 2358.98, 2337.35, 2363.8],
#         [2360.75, 2382.48, 2347.89, 2383.76],
#         [2383.43, 2385.42, 2371.23, 2391.82],
#         [2377.41, 2419.02, 2369.57, 2421.15],
#         [2425.92, 2428.15, 2417.58, 2440.38],
#         [2411, 2433.13, 2403.3, 2437.42],
#         [2432.68, 2334.48, 2427.7, 2441.73],
#         [2430.69, 2418.53, 2394.22, 2433.89],
#         [2416.62, 2432.4, 2414.4, 2443.03],
#         [2441.91, 2421.56, 2418.43, 2444.8],
#         [2420.26, 2382.91, 2373.53, 2427.07],
#         [2383.49, 2397.18, 2370.61, 2397.94],
#         [2378.82, 2325.95, 2309.17, 2378.82],
#         [2322.94, 2314.16, 2308.76, 2330.88],
#         [2320.62, 2325.82, 2315.01, 2338.78],
#         [2313.74, 2293.34, 2289.89, 2340.71],
#         [2297.77, 2313.22, 2292.03, 2324.63],
#         [2322.32, 2365.59, 2308.92, 2366.16],
#         [2364.54, 2359.51, 2330.86, 2369.65],
#         [2332.08, 2273.4, 2259.25, 2333.54],
#         [2274.81, 2326.31, 2270.1, 2328.14],
#         [2333.61, 2347.18, 2321.6, 2351.44],
#         [2340.44, 2324.29, 2304.27, 2352.02],
#         [2326.42, 2318.61, 2314.59, 2333.67],
#         [2314.68, 2310.59, 2296.58, 2320.96],
#         [2309.16, 2286.6, 2264.83, 2333.29],
#         [2282.17, 2263.97, 2253.25, 2286.33],
#         [2255.77, 2270.28, 2253.31, 2276.22],
#     ]
#     # cdata = kline_base(data)
#     cdata = kline_datazoom_inside(data)
#     cdata.render()
#     setText('123455')
#     hwnd = win32gui.FindWindow(None, "微信")
#     ctrlV()
#     altS()
