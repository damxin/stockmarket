# import tushare as ts
# from sqlalchemy import create_engine
# from selenium import webdriver  # 导入Selenium的webdriver
# from selenium.webdriver.common.keys import Keys  # 导入Keys
import pymysql

if __name__ == "__main__":
# import sys;sys.argv = ['', 'Test.testName']
# df = ts.get_hist_data("000001", start='2019-08-22', end='2019-08-31')
# print(df)
# df = ts.get_stock_basics()
# engine = create_engine('mysql+pymysql://root:root@127.0.0.1/stockmarket?charset=utf8')
# df.to_sql('stock_basics', engine, if_exists="replace", index=False)
# print("finish")
# print(df)
# driver = webdriver.Chrome()  # 指定使用的浏览器，初始化webdriver
# driver.get("http://www.python.org")  # 请求网页地址
# assert "Python" in driver.title  # 看看Python关键字是否在网页title中，如果在则继续，如果不在，程序跳出。
# elem = driver.find_element_by_name("q")  # 找到name为q的元素，这里是个搜索框
# elem.clear()  # 清空搜索框中的内容
# elem.send_keys("pycon")  # 在搜索框中输入pycon
# elem.send_keys(Keys.RETURN)  # 相当于回车键，提交
# assert "No results found." not in driver.page_source  # 如果当前页面文本中有“No results found.”则程序跳出
# driver.close()  # 关闭webdriver


#1.创建与数据库连接对象
db =pymysql.connect(host="127.0.0.1",user="root",
                   password="root",database="db4",
                   charset="utf8")

#2.利用db方法创建游标对象
cur = db.cursor()

#3.利用游标对象execute()方法执行SQL命令
#cur.execute(";") #这里填写正确的SQL语句  例如:
cur.execute("insert into sheng values\
            (16,300000,'台湾省');")
#4.提交到数据库执行
db.commit()
print("OK")
#5.关闭游标对象
cur.close()

#6.断开数据库连接
db.close()
————————————————
版权声明：本文为CSDN博主「beBrave_」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/beBrave_/article/details/81408689
