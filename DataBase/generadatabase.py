# -*- coding: utf-8 -*-
'''
   读取 字段及数据结构参考.xlsx，生成对应的数据库表创建脚本及增量脚本
'''

import xlrd

'''
    常量定义
'''
FILE_DIR =".\字段及数据结构参考.xlsx"
VARSHEET = "字段定义"
VARENGNAMECOL = 0
VARTYPECOL = 1
VARCHINAMECOL = 2
VARDICTCOL = 3
VARCOLS = 4
FIRSTVARSTART = "varengname"

'''
    第一个sheet字段读取,前4列
'''
def readvarxlsx(q):
    workbook = xlrd.open_workbook(FILE_DIR)
    booksheet = workbook.sheet_by_name(VARSHEET)
    
    vardict = dict{}
    startflag = 0
    for row in range(booksheet.nrows):            
        cel = booksheet.cell(row, col)
        celreal = cel.lower().trim()
        if celreal in FIRSTVARSTART:
            startflag = 1
        if startflag == 0:
            continue
        
        cel = booksheet.cell(row, VARENGNAMECOL)
        if length(cel.trim()) == 0:
            break
        varEngName = celreal = cel.lower().trim()
        cel = booksheet.cell(row, VARTYPECOL)
        varType = celreal = cel.lower().trim()
        vardict[varEngName] = varType
    xlrd.close_workbook()       
    return vardict

'''
    读取表生成表创建脚本
'''
def generyCreateSql():
    workbook = xlrd.open_workbook(FILE_DIR)
    sizesheet = workbook.sheets().length()
    for indexsheet in range(sizesheet):      
        booksheet = workbook.sheet_by_index(indexsheet+1)

    
if __name__ == '__main__':
    
