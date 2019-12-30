# -*- coding:utf-8 -*-

def yearpdfreadtest(filepath):
    '''
    crawler pypdf的yearpdfread接口测试
    :param filepath:
    :return:
    '''
    import finance.servicelib.crawler.pypdf as pypdf

    pypdf.yearpdfread(filepath)

if __name__ == "__main__":
    yearpdfreadtest("通策医疗：2016年年度报告.PDF")
