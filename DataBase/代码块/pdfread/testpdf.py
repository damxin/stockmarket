import pdfplumber
import pandas as pd

with pdfplumber.open("通策医疗：2016年年度报告.PDF") as pdf:
    '''
    读取pdf的表格
    '''
    # 获取第一页
    first_page = pdf.pages[5]
	
    # 解析文本
    text = first_page.extract_text()
    print(text)
	
    # 解析表格
    tables = first_page.extract_tables()
    for table in tables:
        print(table)
        # df = pd.DataFrame(table[1:], columns=table[0])
        for row in table:
            for cell in row:
                print(cell, end="\t|")
            print()
