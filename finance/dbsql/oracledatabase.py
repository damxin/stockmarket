# -*- coding:utf-8 -*-

import cx_Oracle as oracle  # 这边显示红色是正常的
from finance.dbsql.database import DataBase


class OracleDatabase(DataBase):

    def createConnection(self):
        ##db = oracle.connect('scott/redhat@192.168.223.138:1521/oracle.test')
        ## conn = cx_Oracle.connect("用户名/密码@服务器地址/服务器名") 
        ret = 0
        osqlcon = ""
        cntinfo = self.dbuser + '/' + self.dbpasswd + '@' + self.ipaddr + ':' + self.dbport + '/' + self.databasename
        try:
            #            print("oracle continfo(%s)"% cntinfo)
            osqlcon = oracle.connect(cntinfo)
            self.curcursor = osqlcon.cursor()
            self.connection = osqlcon
        except oracle.DatabaseError as msg:
            ret = 1
            print(msg);
        return ret

    '''
        作用:sql语句执行查询语句,实现分页查询
        select * from (
            select rownum rn,a.* from table_name a where rownum <= x
            //结束行，x = startPage*pageSize
                )
            where rn >= y;
    '''

    def execSelectManySql(self, strsql, ordercause=None):
        endcol = strsql.find("from")
        strmanysql = "select %s from ( select rownum rn, %s where rownum <= %d) a where rn > %d" % (
        strsql[6:endcol], strsql[6:], self.fetchmanystartrow + DataBase.ROWNUM, self.fetchmanystartrow)
        #        print(strmanysql)
        self.curcursor.execute(strmanysql)
        results = self.curcursor.fetchmany(DataBase.ROWNUM)
        retrown = len(results)
        if retrown == 0:
            self.fetchmanystartrow = 0
        else:
            self.fetchmanystartrow = self.fetchmanystartrow + retrown
        return results

    def gettablecol(self, tablename):
        strexecsql = "select cname from col a where upper(a.tname) = upper('%s') order by a.cname" % tablename
        return super().execSelectSmallSql(strexecsql)

    def gettablecolandtype(self, tablename):
        strexecsql = "select cname,coltype from col a where upper(a.tname) = upper('%s') order by a.cname" % tablename
        return super().execSelectSmallSql(strexecsql)

# if __name__ == '__main__':
#    dbcnt = OracleDatabase("192.168.137.131","1521","hs_tabase","hs_tabase","ora11g")
