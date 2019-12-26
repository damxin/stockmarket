import os
import time
import requests
from copy import deepcopy

URL_SSE = "http://www.sse.com.cn/disclosure/listedinfo/announcement/"
# 股票
URL_SSE_STOCK = "http://www.sse.com.cn/js/common/ssesuggestdata.js"
# 基金
URL_SSE_FUND = "http://www.sse.com.cn/js/common/ssesuggestfunddata.js"
# E债券
URL_SSE_EBOND = "http://www.sse.com.cn/js/common/ssesuggestEbonddata.js"
# T债券
URL_SSE_TBOND = "http://www.sse.com.cn/js/common/ssesuggestTbonddata.js"
# 查询
URL_QUERY_COMPANY = "http://query.sse.com.cn/security/stock/queryCompanyBulletin.do"

URL_PDF = "http://static.sse.com.cn"

# 报告类型
REPORT_TYPE = {
    '全部': ('ALL', ''),
    '定期公告': ('ALL', 'DQBG'),
    '年报': ('YEARLY', 'DQBG'),
    '第一季度季报': ('QUATER1', 'DQBG'),
    '半年报': ('QUATER2', 'DQBG'),
    '第三季度季报': ('QUATER3', 'DQBG'),
    '临时公告': ('ALL', 'LSGG'),
    '上市公司章程': ('SHGSZC', 'LSGG'),
    '发行上市公告': ('FXSSGG', 'LSGG'),
    '公司治理': ('GSZL', 'LSGG'),
    '股东大会会议': ('GDDH', 'LSGG'),
    'IPO公司公告': ('IPOGG', 'LSGG'),
    '其他': ('QT', 'LSGG'),
}

# 证券类型
SECURITY_TYPE = {
    '全部': '0101,120100,020100,020200,120200',
    '主板': '0101',
    '科创板': '120100,020100,020200,120200',
}

HEADER = {
    'Referer': URL_SSE,
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

URL_PARAM = {
    # 是否分页
    'isPagination': 'false',
    'productId': '600000',
    # 关键字
    'keyWord': '',
    'securityType': SECURITY_TYPE['全部'],
    'reportType2': 'DQBG',
    'reportType': 'YEARLY',
    'beginDate': '2016-07-17',
    'endDate': '2019-07-17',
}


def get_all_codes(url):
    res = requests.get(url)
    content = res.content.decode()
    tmp = content.split('_t.push({val:"')
    code, name, pinyin = [], [], []
    for i in tmp[1:]:
        item = i.split('"')
        code.append(item[0])
        name.append(item[2])
        pinyin.append(item[4])
    # print(code)
    return code, name, pinyin


def get_pdf_url(code, begin_date, end_date, security_type='全部', report_type='年报'):
    url_param = deepcopy(URL_PARAM)
    url_param['productId'] = code
    url_param['securityType'] = SECURITY_TYPE[security_type]
    url_param['reportType2'] = REPORT_TYPE[report_type][1]
    url_param['reportType'] = REPORT_TYPE[report_type][0]
    url_param['beginDate'] = begin_date
    url_param['endDate'] = end_date
    result = requests.get(URL_QUERY_COMPANY, params=url_param, headers=HEADER).json()['result']
    return [(URL_PDF + i['URL'], i['BULLETIN_TYPE'], i['BULLETIN_YEAR'], i['SSEDATE']) for i in result]


def save_pdf(code, pdf_title_urls, path='./'):
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


def download_report(code):
    month_day = time.strftime('-%m-%d', time.localtime())
    year = int(time.strftime('%Y', time.localtime()))
    while True:
        year_3 = year - 3
        begin_date = str(year_3) + month_day
        end_date = str(year) + month_day
        pdf_urls = get_pdf_url(code, begin_date, end_date)
        # for i in title_urls:
        #     print(i)
        if pdf_urls:
            for i in range(1, 4):
                try:
                    save_pdf(code, pdf_urls)
                    break
                except Exception as e:
                    print(f'[{code}] 第{i}次尝试下载出错', e)
            else:
                print(f'[{code}] 下载失败')
        else:
            print(f'[{code}] 完毕')
            break
        year = year_3
        if year < 1900:
            break


def main():
    stock_codes, _, _ = get_all_codes(URL_SSE_STOCK)
    len_stock_codes = len(stock_codes)
    for index, code in enumerate(stock_codes):
        print(f'股票总数:{len_stock_codes}, 已完成:{index}  ', end='')
        download_report(code)
        break
    print('任务完成')


if __name__ == '__main__':
    main()


