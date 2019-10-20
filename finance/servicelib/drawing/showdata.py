# -*- coding:utf-8 -*-
'''
Created on 2019/10/19
@author: damxin
@group :
@contact: nfx080523@hotmail.com
通过图形的形势展示数据
'''

# #pandas类型转list类型
# data = ts.get_hist_data('300348',start='2017-01-01')
# new_data = data.ix[:,['open','close','high','low']]
# train_data = np.array(new_data)
# train_index = np.array(data.index)

from pyecharts import options as opts
from pyecharts.charts import Kline

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
    tradeDateList = list(tradeDataDf['trade_date'])
    new_data = tradeDataDf.loc[:, gc.PRICE_COLS]
    tradeDataList = np.array(new_data)
    klinedata = (
        Kline()
            .add_xaxis(tradeDateList)
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