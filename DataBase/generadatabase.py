# -*- coding: utf-8 -*-
'''
    author:damxin
    date: 20190905
'''
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
CREATETABLEHEAD="DROP PROCEDURE IF EXISTS sp_db_mysql; \n\
DELIMITER $$ \n\
    CREATE PROCEDURE sp_db_mysql() \n\
        BEGIN \n\
            DECLARE v_rowcount INT; \n\
            DECLARE database_name VARCHAR(100); \n\
            SELECT DATABASE() INTO database_name; \n\
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='%s'; \n\
            IF v_rowcount = 0 THEN \n"
CREATETABLETAIL="\n    );\n\
            END IF; \n\
    END$$ \n\
DELIMITER; \n\
CALL sp_db_mysql(); \n\
DROP PROCEDURE IF EXISTS sp_db_mysql;\n "

ADDVARSQL ="DROP PROCEDURE IF EXISTS sp_db_mysql; \
DELIMITER $$ \
    CREATE PROCEDURE sp_db_mysql()  \
        BEGIN \
            declare v_rowcount int; \
            declare database_name VARCHAR(100); \
            select database() into database_name; \
            select count(1) into v_rowcount from information_schema.columns where table_schema= database_name and table_name='%s' and column_name='%s'; \
            if v_rowcount = 0 then \
                alter table %s add %s %s;\
	    end if; \
	END$$ \
DELIMITER ; \
call sp_db_mysql(); \
DROP PROCEDURE IF EXISTS sp_db_mysql;"



'''
    第一个sheet字段读取,前4列
'''
def readvarxlsx():
    workbook = xlrd.open_workbook(FILE_DIR)
    booksheet = workbook.sheet_by_name(VARSHEET)
    
    vardict = {}
    startflag = 0
    for row in range(booksheet.nrows):            
        cel = booksheet.cell(row, 0).value
        celreal = cel.lower().strip()
        if celreal in FIRSTVARSTART:
            startflag = 1
            continue
        if startflag == 0:
            continue
        
        cel = booksheet.cell(row, VARENGNAMECOL).value
        if len(cel.strip()) == 0:
            break
        varEngName = celreal = cel.lower().strip()
        cel = booksheet.cell(row, VARTYPECOL).value
        varType = celreal = cel.lower().strip()
        vardict[varEngName] = varType

    return vardict

'''
    读取表生成表创建脚本
'''
def generyCreateSql(vardict, outfile):
    workbook = xlrd.open_workbook(FILE_DIR)
    sizesheet = len(workbook.sheets()) - 1
    starttablecol = 0
    starttablerow = 0
    for indexsheet in range(sizesheet):      
        tablesheet = workbook.sheet_by_index(indexsheet+1)
        startflag = 0
        col = 0        
        while col <= tablesheet.ncols and tablesheet.ncols != 0:
            row = 0
            while row <= tablesheet.nrows and tablesheet.nrows != 0:
                print("row:"+str(row))
                print("col:"+str(col))
                cel = tablesheet.cell(row, col).value
                celreal = ""
                if isinstance(cel, float):
                    celreal = str(cel)
                if celreal in TABLENAME:
                    startflag = 1
                    starttablecol = col
                    starttablerow = row
                if startflag == 1:
                    print("打印表名:", end="")
                    print(tablesheet.cell(starttablerow, starttablecol+1).value)
                    gentablename = tablesheet.cell(starttablerow, starttablecol+1).value.lower().strip()
                    createtablesql =CREATETABLEHEAD%gentablename + "    create table " + gentablename + "\n    (\n"
                    # print(createtablesql)
                    for tblrow in range(starttablerow+1, tablesheet.nrows):
                        cel = tablesheet.cell(tblrow, starttablecol).value.strip()                        
                        varEngName = cel.lower().strip()
                        cel = tablesheet.cell(tblrow, starttablecol+1).value
                        varAddFlag = ""
                        if isinstance(cel, float) :
                            varAddFlag = str(cel).split(".")[0]                        
                        varType = vardict[varEngName]
                        print(varAddFlag)
                        if varAddFlag in "0" :
                            createvarsql = "      "+varEngName+" " + varType + ","
                            tmpTableSql = createtablesql + createvarsql                                  
                            createtablesql = tmpTableSql
                        elif varAddFlag in "1" :
                            addvarsql = ADDVARHEAD % (gentablename,varEngName,gentablename,varEngName,varType)
                            print(addvarsql, file=outfile)
                    # 表字段结束                    
                    finallyCreateTableSql = createtablesql[:-1] + CREATETABLETAIL
                    print(finallyCreateTableSql, file=outfile)
                    print("表字段结束")
                    startflag = 0                    
                    break
            col = starttablecol+3
                            
if __name__ == '__main__':
    varDict = readvarxlsx()
    sqlfile = open('out.txt','w')
    generyCreateSql(varDict,sqlfile)
    sqlfile.close()
    
