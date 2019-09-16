# -*- coding:utf-8 -*-

import pymysql as mysql

from finance.dbsql.database import DataBase

class MysqlDatabase(DataBase):

    def createConnection(self):
        msqlcon = ""
        ret = 0
        try:
            msqlcon = mysql.connect(host=self.ipaddr,
                                 user=self.dbuser,
                                 password=self.dbpasswd,
                                 db=self.databasename,
                                 port=int(self.dbport),
                                 charset='gbk')
            self.curcursor = msqlcon.cursor(cursor=mysql.cursors.DictCursor)
#            self.curcursor = msqlcon.cursor()
            self.connection = msqlcon
        except Exception as e:
            ret = 1
            print(e)
        return ret
        
    '''
        作用:sql语句执行查询语句,实现分页查询
    '''
    def execSelectManySql(self,strsql):
        pagestrsql = strsql + " limit "+self.fetchmanystartrow+","+ DataBase.ROWNUM
        self.curcursor.execute(pagestrsql)
        results = self.curcursor.fetchmany(DataBase.ROWNUM)
        retrown = len(results)
        if retrown == 0 :
            self.fetchmanystartrow = 0
        else :
            self.fetchmanystartrow = self.fetchmanystartrow + retrown
        return results
        
    # def gettablecol(self, tablename):
    #     strexecsql = "select column_name from information_schema.columns where table_schema= database() and upper(table_name) = upper('%s') order by column_name" % tablename
    #     print(strexecsql)
    #     return super().execSelectSmallSql(strexecsql)
    #
    # def gettablecolandtype(self, tablename):
    #     strexecsql = "select column_name,data_type from information_schema.columns where table_schema= database() and upper(table_name) = upper('%s') order by column_name" % tablename
    #     print(strexecsql)
    #     return super().execSelectSmallSql(strexecsql)

        
##if __name__ == '__main__':
##    dbcnt = MysqlDatabase("192.168.137.131","3306","root","root","hs_tabase")
##    dbcnt.getConnection()
##    insert_sql = "insert into ta_tfundinfo (c_fundcode, c_tacode, c_tenantid) values (%s, %s, %s)"
##    datalist=[("hello1","F6","*"),("hello2","F6","*")]
##    dbcnt.execInsertMany(insert_sql, datalist)
##    dbcnt.closeDBConnect()
