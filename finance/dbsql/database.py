# -*- coding:utf-8 -*-

class DataBase:
    ROWNUM = 100

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
        self.curcursor.close()
        self.connection.close()

    '''
        一次性插入较多数据量
    '''

    def execInsertMany(self, insert_sql, datalist):
        try:
            self.curcursor.executemany(insert_sql, datalist)  # 注意，第一个参数是None
            self.connection.commit()  # 提交
        except Exception as e:
            print(e)
            self.connection.rollback()

    '''
        作用:sql语句执行查询语句,查询小数据量
    '''

    def execSelectSmallSql(self, strsql):
        try :
            self.curcursor.execute(strsql)
            results = self.curcursor.fetchall()
            return results
        except Exception as e:
            print(strsql)
            print(e)


    def getConnectInfo(self):
        return self.connection

    def getcurcursorInfo(self):
        return self.curcursor
