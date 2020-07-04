# -*- coding:utf-8 -*-

### 数据库连接池

import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from finance.dbsql.database import DataBase
from finance.servicelib.public import public as pb

class DbPool(DataBase):

    # def __init__(self, serverIp, serverPort, serverUser, serverPasswd, serverDb):
    #     self.ipaddr = serverIp
    #     self.dbuser = serverUser
    #     self.dbpasswd = serverPasswd
    #     self.dbport = serverPort
    #     self.databasename = serverDb
    #
    #     host = self.ipaddr,
    #     user = self.dbuser,
    #     password = self.dbpasswd,
    #     db = self.databasename,
    #     port = int(self.dbport)

    def createConnection(self):
        ret = 0
        try:
            maxConnects = pb.getCpuCount() * 2 + 1
            msqlpool = PooledDB(creator=pymysql, maxconnections=maxConnects,
                               mincached=1, maxcached=maxConnects-2,
                               host=self.ipaddr, user=self.dbuser,
                               password=self.dbpasswd, db=self.databasename,
                               port=int(self.dbport), charset='utf8',
                               cursorclass=DictCursor, ###重点注意这里，如果没加此行，则查询表返回数据就是tuple格式，加了此行返回数据就是list字段对应值。
                               blocking=True,use_unicode=True)

            # self.connection = msqlpool.connection(shareable=True)
            # self.curcursor = self.connection.cursor()
            self.connection = None
            self.curcursor = None
            self.dbpool = msqlpool
        except Exception as e:
            ret = 1
            print(e)
        return ret

    def execSelectManySql(self, strsql, ordercause=None):
        '''
            作用:sql语句执行查询语句,实现分页查询
            fetchmany返回的是list(dict)
        '''
        orderby = ordercause if ordercause is not None else ""
        pagestrsql = strsql + orderby + " limit " + str(self.fetchmanystartrow) + "," + str(DataBase.ROWNUM)
        try:
            self.dbconnect = self.dbpool.connection(shareable=True)
            self.curcursor = self.dbconnect.cursor()
            count = self.curcursor.execute(pagestrsql)
            if count > 0:
                results = self.curcursor.fetchall()
            retrown = len(results)
            if retrown == 0:
                self.fetchmanystartrow = 0
            else:
                self.fetchmanystartrow = self.fetchmanystartrow + retrown
            return results
        except Exception as e:
            print(pagestrsql)
            raise RuntimeError("execSelectManySql is error!")
        finally:
            super().closeDBConnect()

    def execInsertManySql(self, strinsertsql, insertlist):
        '''
            作用:sql语句执行插入语句,实现一次插入多条
            insertlist必须是list(list)或者list(tuple)
        '''
        if isinstance(insertlist, list) is False or \
                isinstance(insertlist[0], (tuple, list)) is False:
            print(type(insertlist))
            print(type(insertlist[0]))
            raise RuntimeError("insertlist type is wrong!")
        try:
            self.dbconnect = self.dbpool.connection(shareable=True)
            self.cuccursor = self.dbconnect.cursor()
            self.curcursor.executemany(strinsertsql, insertlist)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(strinsertsql)
            raise RuntimeError("execInsertManySql is error!")
        finally:
            super().closeDBConnect()
