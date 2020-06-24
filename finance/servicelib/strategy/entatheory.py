# -*- coding:utf-8 -*-
'''
   缠论的具体实现
'''

# 实现日线级别的画法。

class EntangLingTheory():

    def __init__(self,prod_code):
        self.prod_code = prod_code

    def gettableindex(self):
        '''
        获取表名的后缀01,02,...,32
        :return:
        '''

    def klinemerge(self):
        '''
        k线做合并，就是处理前后的包含关系
        处理完毕后需要写入到表entdaytradedata01,entdaytradedata02,...entdaytradedata32
        klinedata
        :return:
        '''