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
TABLENAME = "tablename"
CREATETABLEHEAD="DROP PROCEDURE IF EXISTS sp_db_mysql; DELIMITER $$ CREATE PROCEDURE sp_db_mysql() BEGIN  DECLARE v_rowcount INT;  DECLARE database_name VARCHAR(100);  SELECT DATABASE() INTO database_name;  SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='%s';  IF v_rowcount = 0 THEN"
CREATETABLETAIL="END IF;  END$$ DELIMITER ; CALL sp_db_mysql(); DROP PROCEDURE IF EXISTS sp_db_mysql;"
ADDVARHEAD = "DROP PROCEDURE IF EXISTS sp_db_mysql; \
DELIMITER $$ \
	CREATE PROCEDURE sp_db_mysql() \
		BEGIN \
			declare v_rowcount int; \
			declare database_name VARCHAR(100); \
			select database() into database_name; \
			select count(1) into v_rowcount from information_schema.columns where table_schema= database_name and table_name='%s' and column_name='%s'; \
			if v_rowcount = 0 then"
ADDVARTAIL = "end if; \
		END$$ \
DELIMITER ; \
	call sp_db_mysql(); \
DROP PROCEDURE IF EXISTS sp_db_mysql;"

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
def generyCreateSql(vardict):
    workbook = xlrd.open_workbook(FILE_DIR)
    sizesheet = workbook.sheets().length() - 1
    starttablecol = 0
    starttablerow = 0
    for indexsheet in range(sizesheet):      
        tablesheet = workbook.sheet_by_index(indexsheet+1)
        startflag = 0
        for col in range(tablesheet.ncols):
            for row in range(tablesheet.nrows):
                cel = tablesheet.cell(row, col)
                celreal = cel.lower().trim()
                if celreal in TABLENAME:
                    startflag = 1
                    starttablecol = col
                    starttablerow = row
                if startflag == 1:                    
                    gentablename = tablesheet.cell(starttablerow, starttablecol+1)
                    createtablesql = CREATETABLEHEAD % gentablename
                    for tblrow in range(starttablerow, tablesheet.nrows):
                        cel = tablesheet.cell(tblrow, starttablecol)
                        varName = cel.lower().trim()
                        cel = tablesheet.cell(tblrow, starttablecol+1)
                        varAddFlag = cel.lower().trim()
                    
            
            
    
if __name__ == '__main__':
    
