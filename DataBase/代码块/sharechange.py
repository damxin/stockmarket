# -*- coding:utf-8 -*-


import os
import shutil
import datetime
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email.mime.text import MIMEText
# from email import encoders
import random

import requests
from bs4 import BeautifulSoup

download_baseurl = "http://disc.static.szse.cn/download"
# attachPath关键字对应的/disc/disk02/finalpage/2019-12-28/f6dabbc0-d493-442b-95e6-489a76a790b6.PDF
# http://disc.static.szse.cn/download/disc/disk02/finalpage/2019-12-28/f6dabbc0-d493-442b-95e6-489a76a790b6.PDF

# request payload
# {"seDate":["",""],"bigIndustryCode":["A","B"],"channelCode":["listedNotice_disc"],"pageSize":30,"pageNum":1}
# 请选择行业(bigIndustryCode) 农林牧渔:A 采矿业:B ...
# 请选择板块(plateCode)
# {"seDate":["",""],"plateCode":["11"],"channelCode":["listedNotice_disc"],"pageSize":30,"pageNum":1}
# 请选择公告类别(bigCategoryId), 年度报告:010310
# {"seDate":["",""],"plateCode":["11"],"channelCode":["listedNotice_disc"],"bigCategoryId":["010301"],"pageSize":30,"pageNum":1}
# 查找游族网络(002174)
# {"seDate":["",""],"stock":["002174"],"channelCode":["listedNotice_disc"],"pageSize":30,"pageNum":1}
# 选定日期，比如 游族网络，年度报告
#{"seDate":["2018-05-23","2019-12-19"],"stock":["002174"],"channelCode":["listedNotice_disc"],"bigCategoryId":["010301"],"pageSize":30,"pageNum":1}
# announceCount记录公告条数
# 返回的数据具体可见:sharechange.txt

def get_info(start=1,end=1):
    '''
        参考https://blog.csdn.net/kong2030/article/details/83545071
        获取深交所上市公司公告 http://www.szse.cn/disclosure/listed/notice/index.html
    '''

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }

    random_str = str(random.random())
    page_size = 30
    pagenum = 1

    test_url="http://www.szse.cn/api/disc/announcement/detailinfo?random=%s&pageSize=%s&pageNum=%s&plateCode=szse"%(random_str,page_size,pagenum)
    # 发送请求并获取返回数据
    response = requests.get(test_url, headers=headers)
    response.encoding = "utf-8"
    # 获取html网页源码
    # print response.text

    # 首先新建个BeautifulSoup对象，指定html解析器为python标准库自带的html.parser
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup)

if __name__=='__main__':
    get_info(1,1)   #爬取前一百页数据
