# -*- coding:utf-8 -*-
'''
Created on 2019/10/19
@author: damxin
@group :
@contact: nfx080523@hotmail.com
通过图形的形势展示数据
'''



from pyecharts import options as opts
from pyecharts.charts import Kline,Line,Bar
from pyecharts.faker import Faker


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

    # workDateList=['20100101','20100102','20100103','20100104','20100105','20100106','20100107']
    workDateList = [20100101, 20100102, 20100103, 20100104, 20100105, 20100106, 20100107]
    print("workdatelist")
    print(workDateList)
    malist = [50.01,52.03,55.05,50.01,52.03,55.05,48.02]
    print("malist")
    print(list(range(7)))
    line = (
        Line()
            .add_xaxis(workDateList)
            .add_yaxis("kline", malist, is_smooth=True, is_connect_nones=True)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_scale=True),
            yaxis_opts=opts.AxisOpts(is_scale=True),
        )
    )
    line.render("maline.html")
