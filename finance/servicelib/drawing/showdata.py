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
from pyecharts.charts import Kline,Line,Bar,Grid
from pyecharts.faker import Faker

import pandas as pd


from finance.util import GlobalCons as gc
from finance.servicelib.stock import trading as sttradepb

def companybasicinfoanalyce(product_code, showtype=None) -> Grid:
    '''
    公司基础信息展示，营收和净利润的直方图
    :param product_code:
    :param showtype:Y:年，Q:季度，默认为Q
    :return:
    '''
    x_data = ["{}月".format(i) for i in range(1, 13)]
    bar = (
        Bar()
            .add_xaxis(x_data)
            .add_yaxis(
            "蒸发量",
            [2.0, 4.9, 7.0, 23.2, 25.6, 76.7, 135.6, 162.2, 32.6, 20.0, 6.4, 3.3],
            yaxis_index=0,
            color="#d14a61",
        )
            .add_yaxis(
            "降水量",
            [2.6, 5.9, 9.0, 26.4, 28.7, 70.7, 175.6, 182.2, 48.7, 18.8, 6.0, 2.3],
            yaxis_index=1,
            color="#5793f3",
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                name="蒸发量",
                type_="value",
                min_=0,
                max_=250,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            )
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="温度",
                min_=0,
                max_=25,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} °C"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="降水量",
                min_=0,
                max_=250,
                position="right",
                offset=80,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#5793f3")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
            ),
            title_opts=opts.TitleOpts(title="Grid-多 Y 轴示例"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

    line = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis(
            "平均温度",
            [2.0, 2.2, 3.3, 4.5, 6.3, 10.2, 20.3, 23.4, 23.0, 16.5, 12.0, 6.2],
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)

def tradeDataShowKLine(product_code, ma=None, autoType=None) -> Grid:
    '''
    展示该产品的K线图，默认前复权，等值等比例的展示
    :param product_code: 产品代码
    :param ma=[30,60,99,120,250] 均线
    :param autoType: autoType=qfq-前复权 hfq-后复权 None-不复权
    :param *avg_line: 均线   暂时不做
    :return: 
    '''
    ma = [30,60,99,120,250] if ma is None else ma
    (productname,tradeDataDf) = sttradepb.getTradeDataFromDataBase(product_code, ma, autotype=autoType)
    tradeDataDf = tradeDataDf.where(tradeDataDf.notnull(), None)
    workDateList = tradeDataDf['trade_date'].tolist()
    workDateList = list(map(str,workDateList))

    # open,close,low,high数据获取
    new_data = tradeDataDf.loc[:, gc.PRICE_COLS].values
    tradeDataList = new_data.tolist()

    kline = (
        Kline()
            .add_xaxis(xaxis_data=workDateList)
            .add_yaxis(
            series_name="kline",
            y_axis=tradeDataList,
            itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c"),)
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=productname+"(%s)"%product_code,
                subtitle="MA%s"%str(ma),
            ),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            legend_opts=opts.LegendOpts(
                is_show=False, pos_bottom=10, pos_left="center"
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False,
                    type_="inside",
                    xaxis_index=[0, 1],
                    range_start=0,
                    range_end=100,
                ),
                opts.DataZoomOpts(
                    is_show=True,
                    xaxis_index=[0, 1],
                    type_="slider",
                    pos_top="90%",
                    range_start=0,
                    range_end=100,
                ),
            ],
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                background_color="rgba(245, 245, 245, 0.8)",
                border_width=1,
                border_color="#ccc",
                textstyle_opts=opts.TextStyleOpts(color="#000"),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_show=False,
                dimension=2,
                series_index=5,
                is_piecewise=True,
                pieces=[
                    {"value": 1, "color": "#ec0000"},
                    {"value": -1, "color": "#00da3c"},
                ],
            ),
            axispointer_opts=opts.AxisPointerOpts(
                is_show=True,
                link=[{"xAxisIndex": "all"}],
                label=opts.LabelOpts(background_color="#777"),
            ),
            brush_opts=opts.BrushOpts(
                x_axis_index="all",
                brush_link="all",
                out_of_brush={"colorAlpha": 0.1},
                brush_type="lineX",
            ),
        )
    )

    line = (
        Line()
            .add_xaxis(xaxis_data=workDateList)
            .add_yaxis(
            series_name="MA%s"%ma[0],
            y_axis=tradeDataDf.loc[:, 'ma%s'%ma[0]].values.tolist(),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="MA%s"%ma[1],
            y_axis=tradeDataDf.loc[:, 'ma%s'%ma[1]].values.tolist(),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="MA%s"%ma[2],
            y_axis=tradeDataDf.loc[:, 'ma%s'%ma[2]].values.tolist(),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="MA%s"%ma[3],
            y_axis=tradeDataDf.loc[:, 'ma%s'%ma[3]].values.tolist(),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="MA%s" % ma[4],
            y_axis=tradeDataDf.loc[:, 'ma%s'%ma[4]].values.tolist(),
            is_smooth=True,
            is_hover_animation=False,
            linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"))
    )

    bar = (
        Bar()
            .add_xaxis(xaxis_data=workDateList)
            .add_yaxis(
            series_name="Volume",
            yaxis_data=tradeDataDf.loc[:, "volume"].values.tolist(),
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                grid_index=1,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=1,
                is_scale=True,
                split_number=2,
                axislabel_opts=opts.LabelOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    # Kline And Line
    overlap_kline_line = kline.overlap(line)

    # Grid Overlap + Bar
    grid_chart = Grid()
    grid_chart.add(
        overlap_kline_line,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
    )
    grid_chart.add(
        bar,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="8%", pos_top="70%", height="16%"
        ),
    )
    return grid_chart

if __name__ == "__main__":
    product_code = "600763" # 通策医疗
    tradeDataShowKLine(product_code,ma=None,autoType="qfq").render("%s.html"%product_code)

    # overlap_line_scatter().render()
    # x = Faker.choose()
    # print("x")
    # print(x)
    # y= Faker.values()
    # print("y")
    # print(y)
    # line = (
    #     Line()
    #         .add_xaxis(x)
    #         .add_yaxis("商家B", y)
    # )
    # line.render("line.html")
    #
    # # workDateList=['20100101','20100102','20100103','20100104','20100105','20100106','20100107']
    # workDateList = [0,1,2,3,4,5,6,7,8,20100101, 20100102, 20100103, 20100104, 20100105, 20100106, 20100107]
    # print("workdatelist")
    # print(workDateList)
    # malist = [50.01,52.03,55.05,50.01,52.03,55.05,48.02]
    # print("malist")
    # print(list(range(7)))
    # line = (
    #     Line()
    #         .add_xaxis(workDateList)
    #         # .add_xaxis(workDateList)
    #         .add_yaxis("kline", malist, is_smooth=True, is_connect_nones=True)
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
    # line.render("maline.html")
