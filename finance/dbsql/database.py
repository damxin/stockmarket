# -*- coding:utf-8 -*-

class DataBase:
    ROWNUM = 1000

    def __init__(self, serverip, serverport, username, passwd, databasename):
        self.ipaddr = serverip
        self.dbport = serverport
        self.dbuser = username
        self.dbpasswd = passwd
        self.databasename = databasename
        self.fetchmanystartrow = 0

    '''
    作用:关闭数据库连接，与getMysqlConnect成对使用
    '''

    def closeDBConnect(self):
        if self.curcursor is not None:
            self.curcursor.close()
            self.curcursor = None
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        if self.dbpool is not None:
            self.dbpool.close()

    def execInsertMany(self, insert_sql, datalist):
        '''
            一次性插入较多数据量
        '''
        try:
            if self.dbpool is not None:
                self.connection = self.dbpool.connection(shareable=True)
                self.curcursor = self.connection.cursor()
            self.curcursor.executemany(insert_sql, datalist)  # 注意，第一个参数是None
            self.connection.commit()  # 提交
            return None
        except Exception as e:
            print(e)
            self.connection.rollback()
            return e
        finally:
            if self.dbpool is not None:
                self.closeDBConnect()

    '''
        作用:sql语句执行查询语句,查询小数据量
    '''

    def execSelectSmallSql(self, strsql):
        try:
            if self.dbpool is not None:
                self.connection = self.dbpool.connection(shareable=True)
                self.curcursor = self.connection.cursor()
            self.curcursor.execute(strsql)
            results = self.curcursor.fetchall()
            return results
        except Exception as e:
            print("sql select small执行异常:" + strsql, end='')
            print(e)
            return e
        finally:
            if self.dbpool is not None:
                self.closeDBConnect()

    def execSelectAllSql(self, strsql):
        '''
        一次性获取所有数据量
        :param strsql:
        :return:list[dict]
        '''
        try:
            if self.dbpool is not None:
                self.connection = self.dbpool.connection(shareable=True)
                self.curcursor = self.connection.cursor()
            self.curcursor.execute(strsql)
            results = self.curcursor.fetchall()
            return results
        except Exception as e:
            print("sql select all执行异常:" + strsql, end='')
            print(e)
        finally:
            if self.dbpool is not None:
                self.closeDBConnect()

    def execNotSelectSql(self, strsql):
        '''
         执行删除和更新语句
        :param self:
        :param strsql:
        '''
        try:
            if self.dbpool is not None:
                self.connection = self.dbpool.connection(shareable=True)
                self.curcursor = self.connection.cursor()
            self.curcursor.execute(strsql)
            self.connection.commit()  # 提交
        except Exception as e:
            print(strsql)
            print(e)
            return e
        finally:
            if self.dbpool is not None:
                self.closeDBConnect()
        return None

    def getConnectInfo(self):
        return self.connection

    def getcurcursorInfo(self):
        return self.curcursor
