# -*- coding:utf-8 -*-
'''
Created on 2019/12/28
@author: damxin
@group :
@contact: nfx080523@hotmail.com
@function: 实现从网络上下载pdf，pdf解析,然后写入数据库中
'''

def save_pdf(code, pdf_title_urls, path='./'):
    '''
     实现pdf的下载
    :param code:
    :param pdf_title_urls:
    :param path:
    :return:
    '''
    import os
    import requests

    file_path = os.path.join(path, code)
    if not os.path.isdir(file_path):
        os.makedirs(file_path)
    for url, r_type, year, date in pdf_title_urls:
        date = ''.join(date.split('-'))
        file_name = '_'.join([code, r_type, year, date]) + '.pdf'
        file_full_name = os.path.join(file_path, file_name)
        # print(file_full_name)
        rs = requests.get(url, stream=True)
        with open(file_full_name, "wb") as fp:
            for chunk in rs.iter_content(chunk_size=10240):
                if chunk:
                    fp.write(chunk)

def yearpdfread(pdffilepath):
    '''
    pdf文件读取表格数据
    :param pdffilepath:
    :return:
    '''
    import pdfplumber
    import pandas as pd

    with pdfplumber.open(pdffilepath) as pdf:
        totalpagenum = len(pdf.pages)
        for pageid in range(totalpagenum):
            cur_page = pdf.pages[pageid]
            # 解析表格
            tables = cur_page.extract_tables()
            for table in tables:
                print(table)
                dealtable = []
                lentable = len(table)
                if lentable > 2:
                    adjustflag = False
                    for indtable in range(lentable):
                        strtemp = "".join(table[indtable])
                        if "调整" in strtemp:
                            adjustflag = True
                        if indtable > 2 or adjustflag == True:
                            break
                    # 文件有数据需要调整，以往的数据存在问题。
                    if adjustflag == True:
                        firstlist = table[0]
                        secondlist = table[1]
                        #  ['主要财务指标', '2016年', '2015年', None, '本期比上年同期\n增减(%)', '2014年', None],
                        #  [None, None, '调整后', '调整前', None, '调整后', '调整前']
                        # 调整为['主要财务指标', '2016年', '2015年_调整后', '2015年_调整前', '本期比上年同期\n增减(%)', '2014年_调整后', '2014年_调整前']


                df = pd.DataFrame(table[1:], columns=table[0])
                print(df)
                print(df.iloc[:,0])
                # if "主要财务指标" :
            if pageid > 6 :
                break