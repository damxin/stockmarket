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
from pyecharts.charts import Kline

import pandas as pd


from finance.util import GlobalCons as gc
from finance.servicelib.stock import trading as sttradepb

def tradeDataShowKLine(product_code, autoType=None):
    '''
    展示该产品的K线图，默认前复权，等值等比例的展示
    :param product_code: 产品代码
    :param autoType: autoType=qfq-前复权 hfq-后复权 None-不复权
    :param *avg_line: 均线   暂时不做
    :return: 
    '''
    import numpy as np

    tradeDataDf = sttradepb.getTradeDataFromDataBase(product_code,autotype=autoType)
    workDateList = list(tradeDataDf['trade_date'])
    new_data = tradeDataDf.loc[:, gc.PRICE_COLS].values
    tradeDataList = new_data.tolist()
    klinedata = (
        Kline()
            .add_xaxis(workDateList)
            .add_yaxis("kline", tradeDataList)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            datazoom_opts=[opts.DataZoomOpts(type_="inside")],
            title_opts=opts.TitleOpts(title=product_code),
        )
    )
    return klinedata

if __name__ == "__main__":
    product_code = "600763" # 通策医疗
    klinedata = tradeDataShowKLine(product_code,"qfq")
    klinedata.render()
