# import tushare as ts
# from sqlalchemy import create_engine
# from selenium import webdriver  # 导入Selenium的webdriver
# from selenium.webdriver.common.keys import Keys  # 导入Keys
import pymysql
from pyecharts import options as opts
from pyecharts.charts import Kline

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

if __name__ == "__main__":
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
    data = [
        [3000, 1000, 4000, 5000], #        high
        [2300, 2291.3, 2288.26, 2308.38],
        [2295.35, 2346.5, 2295.35, 2345.92],
        [2347.22, 2358.98, 2337.35, 2363.8],
        [2360.75, 2382.48, 2347.89, 2383.76],
        [2383.43, 2385.42, 2371.23, 2391.82],
        [2377.41, 2419.02, 2369.57, 2421.15],
        [2425.92, 2428.15, 2417.58, 2440.38],
        [2411, 2433.13, 2403.3, 2437.42],
        [2432.68, 2334.48, 2427.7, 2441.73],
        [2430.69, 2418.53, 2394.22, 2433.89],
        [2416.62, 2432.4, 2414.4, 2443.03],
        [2441.91, 2421.56, 2418.43, 2444.8],
        [2420.26, 2382.91, 2373.53, 2427.07],
        [2383.49, 2397.18, 2370.61, 2397.94],
        [2378.82, 2325.95, 2309.17, 2378.82],
        [2322.94, 2314.16, 2308.76, 2330.88],
        [2320.62, 2325.82, 2315.01, 2338.78],
        [2313.74, 2293.34, 2289.89, 2340.71],
        [2297.77, 2313.22, 2292.03, 2324.63],
        [2322.32, 2365.59, 2308.92, 2366.16],
        [2364.54, 2359.51, 2330.86, 2369.65],
        [2332.08, 2273.4, 2259.25, 2333.54],
        [2274.81, 2326.31, 2270.1, 2328.14],
        [2333.61, 2347.18, 2321.6, 2351.44],
        [2340.44, 2324.29, 2304.27, 2352.02],
        [2326.42, 2318.61, 2314.59, 2333.67],
        [2314.68, 2310.59, 2296.58, 2320.96],
        [2309.16, 2286.6, 2264.83, 2333.29],
        [2282.17, 2263.97, 2253.25, 2286.33],
        [2255.77, 2270.28, 2253.31, 2276.22],
    ]
    # cdata = kline_base(data)
    cdata = kline_datazoom_inside(data)
    cdata.render()

