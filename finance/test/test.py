import tushare as ts
from sqlalchemy import create_engine

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    # df = ts.get_hist_data("000001", start='2019-08-22', end='2019-08-31')
    # print(df)
    df = ts.get_stock_basics()
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1/stockmarket?charset=utf8')
    df.to_sql('stock_basics', engine, if_exists="replace", index=False)
    print("finish")
    # print(df)
