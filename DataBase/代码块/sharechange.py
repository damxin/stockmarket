# -*- coding:utf-8 -*-


import os
import shutil
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import random

import requests
from bs4 import BeautifulSoup



random_str = str(random.random())
        page_size = 30
        requst_url = "http://www.szse.cn/api/disc/info/find/tannInfo?random=%s&type=2&pageSize=%s&pageNum=%s"%(random_str, page_size, str(i))




def get_info(start=1,end=1):
    '''
        参考https://blog.csdn.net/kong2030/article/details/83545071
        获取深交所上市公司公告
    '''
    info = {}  #储存目标数据
    base_url = "http://www.sse.com.cn" #目标链接
    notice_url = "/disclosure/listed/notice/index.html"
    
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }

    random_str = str(random.random())
    # 上市公司公告
    page_size = 30
    pagenum = 1
    test_url="http://www.szse.cn/api/disc/announcement/detailinfo?random=%s&pageSize=%s&pageNum=%s&plateCode=szse"%(random_str,)
    # 发送请求并获取返回数据
    response = requests.get(base_url+notice_url, headers=headers)
    response.encoding = "utf-8"
    # 获取html网页源码
    # print response.text

    # 首先新建个BeautifulSoup对象，指定html解析器为python标准库自带的html.parser
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup)


get_info(1,1)   #爬取前一百页数据 
