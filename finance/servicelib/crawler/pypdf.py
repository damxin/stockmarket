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

