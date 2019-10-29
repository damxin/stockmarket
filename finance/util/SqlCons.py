# -*- coding:utf-8 -*-
'''
Created on 2019/09/04
@author: damxin
@group :
@contact: nfx080523@hotmail.com
'''

# 表名:逻辑名 与finance.xml的逻辑名一致
LOGICNAME_TMPBASE = "tmpbase"
LOGICNAME_DBBASE = "dbbase"
LOGICNAME_TRADE = "trade"
TABLEDICT = {"stock_basics": LOGICNAME_TMPBASE,
             "productbasicinfo": LOGICNAME_DBBASE,
             "histtradedata": LOGICNAME_TMPBASE,
             "producttradedata": LOGICNAME_TRADE,
             "trade_cal":LOGICNAME_TMPBASE,
             "openday":LOGICNAME_DBBASE,
             "stock_basics_tspro":LOGICNAME_TMPBASE,
             "profit_divis":LOGICNAME_TMPBASE,
             "histprofitdata":LOGICNAME_TMPBASE,
             "histadjfactor":LOGICNAME_TMPBASE,
             "histincome":LOGICNAME_TMPBASE,
             "company_income":LOGICNAME_TRADE}

## 工作日begin
WORKDAY_MAXDATESQL = "select max(trade_date) maxtradedate, exchange_code exchangecode from openday group by exchange_code"
WORKDAY_SQL="select exchange exchange_code, cal_date trade_date, \
 is_open trade_flag from trade_cal where cal_date > %d and exchange = '%s' "

WORKDAY_INSERTSQL = "insert into openday(exchange_code, trade_date, trade_flag) values (%s, %s, %s)"
## 工作日end


## 获取表productdatabaserule数据
DATABASERULE_SQL="select min_product_code minproductcode, max_product_code maxproductcode, \
min_trade_date mintradedate, max_trade_date maxtradedate, logic_name logicname from productdatabaserule \
 where pooltype = '1' "

# 产品相关表数据 begin
PRODUCTBASICINFO_SQL = "SELECT DISTINCT a.code product_code, a.name product_name, '1' product_type, \
       '1' money_type, a.area product_area, a.industry product_industry, \
       a.name product_fullname, LEFT(a.code,3) market_type, '0' exchange_code, \
       'L' ipo_status,a.timeToMarket listed_date, 0 delisted_date \
  FROM stock_basics a"

PRODUCTBASICINFO_INSERTSQL = "insert into productbasicinfo(product_code,product_name,product_type, \
money_type, product_area, product_industry, \
product_fullname, market_type, exchange_code, \
ipo_status,listed_date,delisted_date) values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

PRODUCTBASICINFO_GETSQL = "SELECT product_code, product_name, product_type, \
       money_type, product_area, product_industry, \
       product_fullname, market_type, exchange_code, \
       ipo_status,listed_date, delisted_date \
  FROM productbasicinfo "

CURPRODUCTBASICINFO_GETSQL = "SELECT product_code, product_name, product_type, \
       money_type, product_area, product_industry, \
       product_fullname, market_type, exchange_code, \
       ipo_status,listed_date, delisted_date \
  FROM productbasicinfo \
 where product_code = '%s' "
# 产品相关表信息 end
COMPANYBALANCESHEET_SQL = ""
COMPANYBALANCESHEET_INSERTSQL = ""

# 与每日交易数据相关 begin
PRODUCTMAXTRADEDATE_SQL = " select ifnull(max(trade_date),0) maxtradedate from producttradedata where product_code = '%s' "
## 从tusharep中获取数据
PRODUCTHISTTRADEDATATUSHARE_SQL = " select %s product_code,a.date trade_date, a.open open_price,high high_price, close close_price,\
low low_price, volume product_volume,amount product_amount from histtradedata a "

## 从tusharepro中获取数据
PRODUCTHISTTRADEDATATUSHAREPRO_SQL = " select left(a.ts_code,6) product_code,a.trade_date trade_date, a.open open_price,a.high high_price, a.close close_price,\
a.low low_price, a.vol product_volume,a.amount product_amount from %s a "

PRODUCTTRADEDATA_INSERTSQL = "insert into producttradedata(product_code,trade_date,open_price, \
high_price, close_price, low_price, \
product_volume, product_amount) values ( %s, %s, %s, %s, %s, %s, %s, %s)"

PRODUCTTRADEDATA_GETALLDATA_SQL=" select trade_date, open_price open, close_price close,\
 low_price low, high_price high, product_volume volume \
from producttradedata where product_code = '%s' order by trade_date"

# 与每日交易数据相关 end

# 公司相关的会计数据  being
COMPANYMAXREPORTDATE_SQL = "select ifnull(max(report_date),0) maxreportdate from %s where product_code = '%s' "
INCOMEHIST_SELECTSQL = " SELECT LEFT(ts_code,6) product_code, ann_date announce_date, f_ann_date f_announce_date,\
end_date report_date, \
CASE WHEN report_type = '1' THEN '合并报表' \
WHEN report_type = '2' THEN '单季合并' \
WHEN report_type = '3' THEN '调整单季合并表' \
WHEN report_type = '4' THEN '调整合并报表' \
WHEN report_type = '5' THEN '调整前合并报表' \
WHEN report_type = '6' THEN '母公司报表' \
WHEN report_type = '7' THEN '母公司单季表' \
WHEN report_type = '8' THEN '母公司调整单季表' \
WHEN report_type = '9' THEN '母公司调整表' \
WHEN report_type = '10' THEN '母公司调整前报表' \
WHEN report_type = '11' THEN '调整前合并报表' \
WHEN report_type = '12' THEN '母公司调整前报表' \
ELSE '报表不明' END  report_type, \
CASE WHEN comp_type = '1' THEN '一般工商业' \
WHEN comp_type = '2' THEN '银行' \
WHEN comp_type = '3' THEN '保险' \
WHEN comp_type = '4' THEN '证券' \
ELSE '一般工商业' END company_type, \
basic_eps, diluted_eps, total_revenue, revenue, int_income,\
prem_earned,comm_income,n_commis_income,n_oth_income,n_oth_b_income,\
prem_income,out_prem,une_prem_reser,reins_income,n_sec_tb_income,n_sec_uw_income,\
n_asset_mg_income,oth_b_income,fv_value_chg_gain,invest_income,ass_invest_income,\
forex_gain,total_cogs,oper_cost,int_exp,comm_exp,\
biz_tax_surchg,sell_exp,admin_exp,fin_exp,assets_impair_loss,\
prem_refund,compens_payout,reser_insur_liab,div_payt,reins_exp,\
oper_exp,compens_payout_refu,insur_reser_refu,reins_cost_refund,other_bus_cost,\
operate_profit,non_oper_income,non_oper_exp,nca_disploss,total_profit,\
income_tax,n_income,n_income_attr_p,minority_gain,oth_compr_income,\
t_compr_income,compr_inc_attr_p,compr_inc_attr_m_s,ebit,ebitda,\
insurance_exp,undist_profit,distable_profit,'1' update_flag \
FROM %s "
CASHFLOWHIST_SELECTSQL = ""
BALANCEHIST_SELECTSQL = ""
COMPANYFINANCE_SELECTSQL = {"company_income":INCOMEHIST_SELECTSQL,
                            "company_cashflow":CASHFLOWHIST_SELECTSQL,
                            "company_balance_sheet":BALANCEHIST_SELECTSQL}
INCOME_INSERTSQL = "INSERT INTO company_income \
(product_code, announce_date, f_announce_date, report_date, report_type,\
 company_type, basic_eps, diluted_eps, total_revenue, revenue,\
 int_income, prem_earned, comm_income, n_commis_income, n_oth_income,\
 n_oth_b_income, prem_income, out_prem, une_prem_reser, reins_income,\
 n_sec_tb_income, n_sec_uw_income, n_asset_mg_income, oth_b_income, fv_value_chg_gain,\
 invest_income, ass_invest_income, forex_gain, total_cogs, oper_cost,\
 int_exp, comm_exp, biz_tax_surchg, sell_exp, admin_exp,\
 fin_exp, assets_impair_loss, prem_refund, compens_payout, reser_insur_liab,\
 div_payt, reins_exp, oper_exp, compens_payout_refu, insur_reser_refu,\
 reins_cost_refund, other_bus_cost, operate_profit, non_oper_income, non_oper_exp,\
 nca_disploss, total_profit, income_tax, n_income, n_income_attr_p,\
 minority_gain, oth_compr_income, t_compr_income, compr_inc_attr_p, compr_inc_attr_m_s,\
 ebit, ebitda, insurance_exp, undist_profit, distable_profit, update_flag)\
 VALUES (%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,%s)"
CASHFLOW_INSERTSQL = ""
BALANCE_INSERTQL = ""
COMPANYFINANCE_INSERTSQL = {"company_income":INCOME_INSERTSQL,
                            "company_cashflow":CASHFLOW_INSERTSQL,
                            "company_balance_sheet":BALANCE_INSERTQL}
# 公司相关的会计数据 end