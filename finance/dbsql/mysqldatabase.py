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
            self.dbpool = None
        except Exception as e:
            ret = 1
            print(e)
        return ret

    '''
        作用:sql语句执行查询语句,实现分页查询
        fetchmany返回的是list(dict)
    '''

    def execSelectManySql(self, strsql, ordercause=None):
        orderby = ordercause if ordercause is not None else ""
        pagestrsql = strsql + orderby + " limit " + str(self.fetchmanystartrow) + "," + str(DataBase.ROWNUM)
        try:
            self.curcursor.execute(pagestrsql)
        except Exception as e:
            print(pagestrsql)
            raise RuntimeError("execSelectManySql is error!")
        results = self.curcursor.fetchmany(DataBase.ROWNUM)
        retrown = len(results)
        if retrown == 0:
            self.fetchmanystartrow = 0
        else:
            self.fetchmanystartrow = self.fetchmanystartrow + retrown
        return results

    def execInsertManySql(self, strinsertsql, insertlist):
        '''
                作用:sql语句执行插入语句,实现一次插入多条
                insertlist必须是list(list)或者list(tuple)
        :param strinsertsql:
        :param insertlist:
        :return:
        '''

        if isinstance(insertlist, list) is False or \
                isinstance(insertlist[0], (tuple, list)) is False:
            print(type(insertlist))
            print(type(insertlist[0]))
            raise RuntimeError("insertlist type is wrong!")
        try:
            self.curcursor.executemany(strinsertsql, insertlist)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(strinsertsql)
            raise RuntimeError("execInsertManySql is error!")

    def execupdatemanysql(self, strupdatesql, updatelist):
        '''
                作用:sql语句执行插入语句,实现一次插入多条
                updatelist必须是tuple(tuple)或者list(tuple)
        :param strinsertsql:
        :param insertlist:
        :return:
        '''

        if isinstance(updatelist, list) is False or \
                isinstance(updatelist[0], tuple) is False:
            print(type(updatelist))
            print(type(updatelist[0]))
            raise RuntimeError("updatelist type is wrong!")
        try:
            self.curcursor.executemany(strupdatesql, updatelist)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(strupdatesql)
            raise RuntimeError("execupdatemanysql is error!")

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
