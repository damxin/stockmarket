# -*- coding:utf-8 -*-
'''
Created on 2019/10/19
@author: damxin
@group :
@contact: nfx080523@hotmail.com
通过图形的形势展示数据
'''

# #pandas类型转list类型
# tradeDataDf = pd.DataFrame([[20191011, 1.2, 1.3, 1.15, 1.35],
#                             [20191012, 1.2, 1.3, 1.15, 1.35],
#                             [20191013, 1.2, 1.3, 1.15, 1.35],
#                             [20191014, 1.2, 1.3, 1.15, 1.35]],
#                            columns=['trade_date', 'open', 'close', 'low', 'high'])
# print(tradeDataDf)
# tradeDateList = list(tradeDataDf['trade_date'])
# print("tradeDateList:")
# print(tradeDateList)
# new_data = tradeDataDf.loc[:, gc.PRICE_COLS].values
# print("new_data:")
# print(new_data)
# tradeDataList = new_data.tolist()
# print("tradeDataList:")
# print(tradeDataList)
# print(tradeDataList[0])
# print(type(tradeDataList[0]))

from pyecharts import options as opts
from pyecharts.charts import Kline,Line,Bar
from pyecharts.faker import Faker

import pandas as pd


from finance.util import GlobalCons as gc
from finance.servicelib.stock import trading as sttradepb

def tradeDataShowKLine(product_code, ma=None, autoType=None):
    '''
    展示该产品的K线图，默认前复权，等值等比例的展示
    :param product_code: 产品代码
    :param ma=[30,60,99,120,250] 均线
    :param autoType: autoType=qfq-前复权 hfq-后复权 None-不复权
    :param *avg_line: 均线   暂时不做
    :return: 
    '''
    ma = [30,60,99,120,250] if ma is None else ma
    tradeDataDf = sttradepb.getTradeDataFromDataBase(product_code, ma, autotype=autoType)
    tradeDataDf = tradeDataDf.where(tradeDataDf.notnull(), 50.00)
    workDateList = tradeDataDf['trade_date'].tolist()
    print(workDateList)
    print(len(workDateList))
    # open,close,low,high数据获取
    new_data = tradeDataDf.loc[:, gc.PRICE_COLS].values
    tradeDataList = new_data.tolist()
    # malistkey = []
    # for a in ma :
    #     malistkey.append('ma%s'%a)
    #     break
    new_data = tradeDataDf.loc[:, 'ma%s'%ma[0]].values
    malist = new_data.tolist()
    print("malist:")
    print(malist)
    print(len(malist))

    # title = product_code+" 日K线图"
    # klinedata = (
    #     Kline()
    #         .add_xaxis(workDateList)
    #         .add_yaxis("kline", tradeDataList)
    #         .set_global_opts(
    #         xaxis_opts=opts.AxisOpts(is_scale=True),
    #         yaxis_opts=opts.AxisOpts(
    #             is_scale=True,
    #             splitarea_opts=opts.SplitAreaOpts(
    #                 is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
    #             ),
    #         ),
    #         datazoom_opts=[opts.DataZoomOpts(type_="inside")],
    #         title_opts=opts.TitleOpts(title=title),
    #     )
    # )
    workDateList=[20100101,20100102,20100103]
    malist = [50.01,52.03,55.05]
    maline = (
        Line()
            .add_xaxis(workDateList)
            .add_yaxis("kline", malist, is_smooth=True, is_connect_nones=True)
    )
    maline.render("maline.html")
    # klinedata.overlap(maline)

    # return klinedata

def overlap_line_scatter() -> Bar:
    x = Faker.choose()
    print(x)
    y= Faker.values()
    print(y)
    bar = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("商家A", y)
            .set_global_opts(title_opts=opts.TitleOpts(title="Overlap-line+scatter"))
    )
    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis("商家A", y)
    )
    line.render("line.html")
    bar.overlap(line)
    return bar

if __name__ == "__main__":
    # product_code = "600763" # 通策医疗
    # tradeDataShowKLine(product_code,ma=None,autoType="qfq")
    # overlap_line_scatter().render()
    x = Faker.choose()
    print("x")
    print(x)
    y= Faker.values()
    print("y")
    print(y)
    line = (
        Line()
            .add_xaxis(x)
            .add_yaxis("商家B", y)
    )
    line.render("line.html")

    workDateList=['20100101','20100102','20100103','20100104','20100105','20100106','20100107']
    print("workdatelist")
    print(workDateList)
    malist = [50.01,52.03,55.05,50.01,52.03,55.05,48.02]
    print("malist")
    print(list(range(7)))
    line = (
        Line()
            .add_xaxis(list(range(7)))
            # .add_xaxis(workDateList)
            .add_yaxis("kline", malist, is_smooth=True, is_connect_nones=True)
    )
    line.render("maline.html")
