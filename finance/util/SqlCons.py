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
TABLEDICT = {
            "stock_basics": LOGICNAME_TMPBASE,
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
             "company_income":LOGICNAME_TRADE,
             "histcastflow":LOGICNAME_TMPBASE,
             "company_cashflow":LOGICNAME_TRADE,
             "histbalance":LOGICNAME_TMPBASE,
             "company_balance_sheet":LOGICNAME_TRADE,
             "datadownloadlog":LOGICNAME_TRADE,
             "entdaytradedata":LOGICNAME_TRADE,
             "prod30tradedata":LOGICNAME_TRADE
            }
# 表名:单表拆分的表个数
SPLITTBLDICT = {"entdaytradedata":32, "ent30tradedata":32}

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
CASE WHEN report_type = '1' THEN '1:合并报表' \
WHEN report_type = '2' THEN '2:单季合并' \
WHEN report_type = '3' THEN '3:调整单季合并表' \
WHEN report_type = '4' THEN '4:调整合并报表' \
WHEN report_type = '5' THEN '5:调整前合并报表' \
WHEN report_type = '6' THEN '6:母公司报表' \
WHEN report_type = '7' THEN '7:母公司单季表' \
WHEN report_type = '8' THEN '8:母公司调整单季表' \
WHEN report_type = '9' THEN '9:母公司调整表' \
WHEN report_type = '10' THEN '10:母公司调整前报表' \
WHEN report_type = '11' THEN '11:调整前合并报表' \
WHEN report_type = '12' THEN '12:母公司调整前报表' \
ELSE '99:报表不明' END  report_type, \
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
insurance_exp,undist_profit,distable_profit,'0' update_flag \
FROM %s where end_date > %d order by end_date asc "

BALANCEHIST_SELECTSQL = "SELECT LEFT(ts_code,6) product_code, ann_date announce_date,f_ann_date f_announce_date,\
end_date report_date, \
CASE WHEN report_type = '1' THEN '1:合并报表' \
WHEN report_type = '2' THEN '2:单季合并' \
WHEN report_type = '3' THEN '3:调整单季合并表' \
WHEN report_type = '4' THEN '4:调整合并报表' \
WHEN report_type = '5' THEN '5:调整前合并报表' \
WHEN report_type = '6' THEN '6:母公司报表' \
WHEN report_type = '7' THEN '7:母公司单季表' \
WHEN report_type = '8' THEN '8:母公司调整单季表' \
WHEN report_type = '9' THEN '9:母公司调整表' \
WHEN report_type = '10' THEN '10:母公司调整前报表' \
WHEN report_type = '11' THEN '11:调整前合并报表' \
WHEN report_type = '12' THEN '12:母公司调整前报表' \
ELSE '99:报表不明' END  report_type, \
CASE WHEN comp_type = '1' THEN '一般工商业' \
WHEN comp_type = '2' THEN '银行' \
WHEN comp_type = '3' THEN '保险' \
WHEN comp_type = '4' THEN '证券' \
ELSE '一般工商业' END company_type, \
total_share, cap_rese,undistr_porfit undistr_profit,surplus_rese,special_rese,money_cap,\
trad_asset trade_asset,notes_receiv notes_willreceiv,accounts_receiv accounts_willreceiv,\
oth_receiv other_willreceiv,prepayment,div_receiv dividend_willreceiv,int_receiv interest_willreceiv,\
inventories,amor_exp,nca_within_1y notcash_within_1y,sett_rsrv,loanto_oth_bank_fi,\
premium_receiv,reinsur_receiv,reinsur_res_receiv,pur_resale_fa,oth_cur_assets,\
total_cur_assets,fa_avail_for_sale,htm_invest,lt_eqt_invest long_stock_invest,\
invest_real_estate,time_deposits,oth_assets,lt_rec long_term_rec,fix_assets,\
cip constr_in_process,const_materials,fixed_assets_disp,produc_bio_assets,\
oil_and_gas_assets,intan_assets,r_and_d study_spending,goodwill,\
lt_amor_exp long_term_amor_exp,defer_tax_assets,decr_in_disbur,oth_nca other_not_cash,\
total_nca total_not_cash,cash_reser_cb,depos_in_oth_bfi,prec_metals,deriv_assets,\
rr_reins_une_prem,rr_reins_outstd_cla,rr_reins_lins_liab,rr_reins_lthins_liab,\
refund_depos,ph_pledge_loans,refund_cap_depos,indep_acct_assets,client_depos,\
client_prov,transac_seat_fee,invest_as_receiv,total_assets,lt_borr long_borrow,\
st_borr short_borrow,cb_borr central_bank_borrow,depos_ib_deposits,loan_oth_bank,\
trading_fl trading_finance_load,notes_payable,acct_payable,adv_receipts,\
sold_for_repur_fa,comm_payable,payroll_payable,taxes_payable,int_payable interst_payable,\
div_payable dividend_payable,oth_payable,acc_exp,deferred_inc,st_bonds_payable,\
payable_to_reinsurer,rsrv_insur_cont,acting_trading_sec,acting_uw_sec,\
non_cur_liab_due_1y,oth_cur_liab,total_cur_liab,bond_payable,lt_payable long_money_payable,\
specific_payables,estimated_liab,defer_tax_liab,defer_inc_non_cur_liab,\
oth_ncl other_not_cur_load,total_ncl total_not_cur_load,depos_oth_bfi,\
deriv_liab,depos,agency_bus_liab,oth_liab,prem_receiv_adva,depos_received,\
ph_invest,reser_une_prem,reser_outstd_claims,reser_lins_liab,reser_lthins_liab,\
indept_acc_liab,pledge_borr,indem_payable,policy_div_payable,total_liab,\
treasury_share,ordin_risk_reser,forex_differ,invest_loss_unconf,minority_int,\
total_hldr_eqy_exc_min_int,total_hldr_eqy_inc_min_int,total_liab_hldr_eqy,\
lt_payroll_payable,oth_comp_income,oth_eqt_tools,oth_eqt_tools_p_shr,lending_funds,\
acc_receivable,st_fin_payable,payables,hfs_assets,hfs_sales,'0' update_flag \
FROM %s where end_date > %d order by end_date asc "

CASHFLOWHIST_SELECTSQL = "SELECT LEFT(ts_code,6) product_code, ann_date announce_date,f_ann_date f_announce_date,\
end_date report_date, \
CASE WHEN report_type = '1' THEN '1:合并报表' \
WHEN report_type = '2' THEN '2:单季合并' \
WHEN report_type = '3' THEN '3:调整单季合并表' \
WHEN report_type = '4' THEN '4:调整合并报表' \
WHEN report_type = '5' THEN '5:调整前合并报表' \
WHEN report_type = '6' THEN '6:母公司报表' \
WHEN report_type = '7' THEN '7:母公司单季表' \
WHEN report_type = '8' THEN '8:母公司调整单季表' \
WHEN report_type = '9' THEN '9:母公司调整表' \
WHEN report_type = '10' THEN '10:母公司调整前报表' \
WHEN report_type = '11' THEN '11:调整前合并报表' \
WHEN report_type = '12' THEN '12:母公司调整前报表' \
ELSE '99:报表不明' END  report_type, \
CASE WHEN comp_type = '1' THEN '一般工商业' \
WHEN comp_type = '2' THEN '银行' \
WHEN comp_type = '3' THEN '保险' \
WHEN comp_type = '4' THEN '证券' \
ELSE '一般工商业' END company_type, \
net_profit, finan_exp, c_fr_sale_sg, recp_tax_rends, n_depos_incr_fi, \
n_incr_loans_cb, n_inc_borr_oth_fi, prem_fr_orig_contr, n_incr_insured_dep, n_reinsur_prem, \
n_incr_disp_tfa, ifc_cash_incr, n_incr_disp_faas, n_incr_loans_oth_bank, n_cap_incr_repur , \
c_fr_oth_operate_a, c_inf_fr_operate_a, c_paid_goods_s, c_paid_to_for_empl, c_paid_for_taxes, \
n_incr_clt_loan_adv, n_incr_dep_cbob, c_pay_claims_orig_inco, pay_handling_chrg, pay_comm_insur_plcy, \
oth_cash_pay_oper_act, st_cash_out_act, n_cashflow_act, oth_recp_ral_inv_act, c_disp_withdrwl_invest, \
c_recp_return_invest, n_recp_disp_fiolta, n_recp_disp_sobu, stot_inflows_inv_act, c_pay_acq_const_fiolta, \
c_paid_invest, n_disp_subs_oth_biz, oth_pay_ral_inv_act, n_incr_pledge_loan, stot_out_inv_act, \
n_cashflow_inv_act, c_recp_borrow, proc_issue_bonds, oth_cash_recp_ral_fnc_act, stot_cash_in_fnc_act, \
free_cashflow, c_prepay_amt_borr, c_pay_dist_dpcp_int_exp, incl_dvd_profit_paid_sc_ms, oth_cashpay_ral_fnc_act, \
stot_cashout_fnc_act, n_cash_flows_fnc_act, eff_fx_flu_cash, n_incr_cash_cash_equ, c_cash_equ_beg_period, \
c_cash_equ_end_period, c_recp_cap_contrib, incl_cash_rec_saims, uncon_invest_loss, prov_depr_assets, \
depr_fa_coga_dpba, amort_intang_assets, lt_amort_deferred_exp, decr_deferred_exp, incr_acc_exp, \
loss_disp_fiolta, loss_scr_fa, loss_fv_chg, invest_loss, decr_def_inc_tax_assets, \
incr_def_inc_tax_liab, decr_inventories, decr_oper_payable, incr_oper_payable, others others_payable, \
conv_debt_into_cap, conv_copbonds_due_within_1y, fa_fnc_leases, end_bal_cash, beg_bal_cash, \
end_bal_cash_equ, beg_bal_cash_equ, im_n_incr_cash_equ, '0' update_flag \
FROM %s where end_date > %d order by end_date asc "
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
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,%s)"

BALANCE_INSERTQL = "insert into company_balance_sheet\
(product_code,announce_date,f_announce_date,report_date,report_type,\
company_type,total_share,cap_rese,undistr_profit,surplus_rese,\
special_rese,money_cap,trade_asset,notes_willreceiv,accounts_willreceiv,\
other_willreceiv,prepayment,dividend_willreceiv,interest_willreceiv,inventories,\
amor_exp,notcash_within_1y,sett_rsrv,loanto_oth_bank_fi,premium_receiv,\
reinsur_receiv,reinsur_res_receiv,pur_resale_fa,oth_cur_assets,total_cur_assets,\
fa_avail_for_sale,htm_invest,long_stock_invest,invest_real_estate,time_deposits,\
oth_assets,long_term_rec,fix_assets,constr_in_process,const_materials,\
fixed_assets_disp,produc_bio_assets,oil_and_gas_assets,intan_assets,study_spending,\
goodwill,long_term_amor_exp,defer_tax_assets,decr_in_disbur,other_not_cash,\
total_not_cash,cash_reser_cb,depos_in_oth_bfi,prec_metals,deriv_assets,\
rr_reins_une_prem,rr_reins_outstd_cla,rr_reins_lins_liab,rr_reins_lthins_liab,refund_depos,\
ph_pledge_loans,refund_cap_depos,indep_acct_assets,client_depos,client_prov,\
transac_seat_fee,invest_as_receiv,total_assets,long_borrow,short_borrow,\
central_bank_borrow,depos_ib_deposits,loan_oth_bank,trading_finance_load,notes_payable,\
acct_payable,adv_receipts,sold_for_repur_fa,comm_payable,payroll_payable,\
taxes_payable,interst_payable,dividend_payable,oth_payable,acc_exp,\
deferred_inc,st_bonds_payable,payable_to_reinsurer,rsrv_insur_cont,acting_trading_sec,\
acting_uw_sec,non_cur_liab_due_1y,oth_cur_liab,total_cur_liab,bond_payable,\
long_money_payable,specific_payables,estimated_liab,defer_tax_liab,defer_inc_non_cur_liab,\
other_not_cur_load,total_not_cur_load,depos_oth_bfi,deriv_liab,depos,\
agency_bus_liab,oth_liab,prem_receiv_adva,depos_received,ph_invest,\
reser_une_prem,reser_outstd_claims,reser_lins_liab,reser_lthins_liab,indept_acc_liab,\
pledge_borr,indem_payable,policy_div_payable,total_liab,treasury_share,\
ordin_risk_reser,forex_differ,invest_loss_unconf,minority_int,total_hldr_eqy_exc_min_int,\
total_hldr_eqy_inc_min_int,total_liab_hldr_eqy,lt_payroll_payable,oth_comp_income,oth_eqt_tools,\
oth_eqt_tools_p_shr,lending_funds,acc_receivable,st_fin_payable,payables,\
hfs_assets,hfs_sales,update_flag) \
value (%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s,%s,%s,\
%s,%s,%s)"

CASHFLOW_INSERTSQL = "INSERT INTO company_cashflow \
(product_code, announce_date, f_announce_date, report_date, report_type, company_type, \
net_profit, finan_exp, c_fr_sale_sg, recp_tax_rends, n_depos_incr_fi, \
n_incr_loans_cb, n_inc_borr_oth_fi, prem_fr_orig_contr, n_incr_insured_dep, n_reinsur_prem, \
n_incr_disp_tfa, ifc_cash_incr, n_incr_disp_faas, n_incr_loans_oth_bank, n_cap_incr_repur, \
c_fr_oth_operate_a, c_inf_fr_operate_a, c_paid_goods_s, c_paid_to_for_empl, c_paid_for_taxes, \
n_incr_clt_loan_adv, n_incr_dep_cbob, c_pay_claims_orig_inco, pay_handling_chrg, pay_comm_insur_plcy, \
oth_cash_pay_oper_act, st_cash_out_act, n_cashflow_act, oth_recp_ral_inv_act, c_disp_withdrwl_invest, \
c_recp_return_invest, n_recp_disp_fiolta, n_recp_disp_sobu, stot_inflows_inv_act, c_pay_acq_const_fiolta, \
c_paid_invest, n_disp_subs_oth_biz, oth_pay_ral_inv_act, n_incr_pledge_loan, stot_out_inv_act, \
n_cashflow_inv_act, c_recp_borrow, proc_issue_bonds, oth_cash_recp_ral_fnc_act, stot_cash_in_fnc_act, \
free_cashflow, c_prepay_amt_borr, c_pay_dist_dpcp_int_exp, incl_dvd_profit_paid_sc_ms, oth_cashpay_ral_fnc_act, \
stot_cashout_fnc_act, n_cash_flows_fnc_act, eff_fx_flu_cash, n_incr_cash_cash_equ, c_cash_equ_beg_period, \
c_cash_equ_end_period, c_recp_cap_contrib, incl_cash_rec_saims, uncon_invest_loss, prov_depr_assets, \
depr_fa_coga_dpba, amort_intang_assets, lt_amort_deferred_exp, decr_deferred_exp, incr_acc_exp, \
loss_disp_fiolta, loss_scr_fa, loss_fv_chg, invest_loss, decr_def_inc_tax_assets, \
incr_def_inc_tax_liab, decr_inventories, decr_oper_payable, incr_oper_payable, others_payable, \
conv_debt_into_cap, conv_copbonds_due_within_1y, fa_fnc_leases, end_bal_cash, beg_bal_cash, \
end_bal_cash_equ, beg_bal_cash_equ, im_n_incr_cash_equ, update_flag) \
values (%s, %s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s, %s, \
%s, %s, %s, %s)"
COMPANYFINANCE_INSERTSQL = {"company_income":INCOME_INSERTSQL,
                            "company_cashflow":CASHFLOW_INSERTSQL,
                            "company_balance_sheet":BALANCE_INSERTQL}

# 正式表中的数据获取,获取出的数据进行处理
INCOME_PUBYEARSELECTSQL = "SELECT a.product_code,a.announce_date,a.f_announce_date,a.report_type,a.report_date,\
a.company_type,a.basic_eps,a.diluted_eps,a.total_revenue,a.revenue,\
a.int_income,a.prem_earned,a.comm_income,a.n_commis_income,a.n_oth_income,\
a.n_oth_b_income,a.prem_income,a.out_prem,a.une_prem_reser,a.reins_income,\
a.n_sec_tb_income,a.n_sec_uw_income,a.n_asset_mg_income,a.oth_b_income,a.fv_value_chg_gain,\
a.invest_income,a.ass_invest_income,a.forex_gain,a.total_cogs,a.oper_cost,\
a.int_exp,a.comm_exp,a.biz_tax_surchg,a.sell_exp,a.admin_exp,\
a.fin_exp,a.assets_impair_loss,a.prem_refund,a.compens_payout,a.reser_insur_liab,\
a.div_payt,a.reins_exp,a.oper_exp,a.compens_payout_refu,a.insur_reser_refu,\
a.reins_cost_refund,a.other_bus_cost,a.operate_profit,a.non_oper_income,a.non_oper_exp,\
a.nca_disploss,a.total_profit,a.income_tax,a.n_income,a.n_income_attr_p,\
a.minority_gain,a.oth_compr_income,a.t_compr_income,a.compr_inc_attr_p,a.compr_inc_attr_m_s, \
a.ebit,a.ebitda,a.insurance_exp,a.undist_profit,a.distable_profit,\
a.update_flag \
FROM (SELECT a.* \
	  FROM company_income a \
	 WHERE a.product_code = '%s' \
	   AND a.report_date %% 10000 = 1231 \
	UNION \
	SELECT a.* \
	  FROM company_income a, \
	       (SELECT MAX(a.report_date) maxreportdate \
		      FROM company_income a \
		     WHERE a.product_code = '%s') b \
	 WHERE a.product_code = '%s' \
	   AND a.report_date = b.maxreportdate) a \
  ORDER BY a.report_date DESC \
  LIMIT %d"
CASHFLOW_PUBYEARSELECTSQL = "SELECT a.product_code,a.announce_date,a.f_announce_date,a.report_date,a.report_type, \
a.company_type,a.net_profit,a.finan_exp,a.c_fr_sale_sg,a.recp_tax_rends, \
a.n_depos_incr_fi,a.n_incr_loans_cb,a.n_inc_borr_oth_fi,a.prem_fr_orig_contr,a.n_incr_insured_dep, \
a.n_reinsur_prem,a.n_incr_disp_tfa,a.ifc_cash_incr,a.n_incr_disp_faas,a.n_incr_loans_oth_bank, \
a.n_cap_incr_repur,a.c_fr_oth_operate_a,a.c_inf_fr_operate_a,a.c_paid_goods_s,a.c_paid_to_for_empl, \
a.c_paid_for_taxes,a.n_incr_clt_loan_adv,a.n_incr_dep_cbob,a.c_pay_claims_orig_inco,a.pay_handling_chrg, \
a.pay_comm_insur_plcy,a.oth_cash_pay_oper_act,a.st_cash_out_act,a.n_cashflow_act,a.oth_recp_ral_inv_act, \
a.c_disp_withdrwl_invest,a.c_recp_return_invest,a.n_recp_disp_fiolta,a.n_recp_disp_sobu,a.stot_inflows_inv_act, \
a.c_pay_acq_const_fiolta,a.c_paid_invest,a.n_disp_subs_oth_biz,a.oth_pay_ral_inv_act,a.n_incr_pledge_loan, \
a.stot_out_inv_act,a.n_cashflow_inv_act,a.c_recp_borrow,a.proc_issue_bonds,a.oth_cash_recp_ral_fnc_act, \
a.stot_cash_in_fnc_act,a.free_cashflow,a.c_prepay_amt_borr,a.c_pay_dist_dpcp_int_exp,a.incl_dvd_profit_paid_sc_ms, \
a.oth_cashpay_ral_fnc_act,a.stot_cashout_fnc_act,a.n_cash_flows_fnc_act,a.eff_fx_flu_cash,a.n_incr_cash_cash_equ, \
a.c_cash_equ_beg_period,a.c_cash_equ_end_period,a.c_recp_cap_contrib,a.incl_cash_rec_saims,a.uncon_invest_loss, \
a.prov_depr_assets,a.depr_fa_coga_dpba,a.amort_intang_assets,a.lt_amort_deferred_exp,a.decr_deferred_exp, \
a.incr_acc_exp,a.loss_disp_fiolta,a.loss_scr_fa,a.loss_fv_chg,a.invest_loss, \
a.decr_def_inc_tax_assets,a.incr_def_inc_tax_liab,a.decr_inventories,a.decr_oper_payable,a.incr_oper_payable, \
a.others_payable,a.conv_debt_into_cap,a.conv_copbonds_due_within_1y,a.fa_fnc_leases,a.end_bal_cash, \
a.beg_bal_cash,a.end_bal_cash_equ,a.beg_bal_cash_equ,a.im_n_incr_cash_equ,a.update_flag \
  FROM (SELECT a.* \
	  FROM company_cashflow a \
	 WHERE a.product_code = '%s' \
	   AND a.report_date %%10000 = 1231 \
	UNION \
	SELECT a.* \
	  FROM company_cashflow a, \
	       (SELECT MAX(a.report_date) maxreportdate \
		  FROM company_balance_sheet a \
		 WHERE a.product_code = '%s') b \
	 WHERE a.product_code = '%s' \
	   AND a.report_date = b.maxreportdate) a \
  ORDER BY a.report_date DESC \
  LIMIT %d"
BALACESHEET_PUBYEARSELECTSQL = "SELECT a.product_code,a.announce_date,a.f_announce_date,a.report_date,a.report_type, \
a.company_type,a.total_share,a.cap_rese,a.undistr_profit,a.surplus_rese, \
a.special_rese,a.money_cap,a.trade_asset,a.notes_willreceiv,a.accounts_willreceiv, \
a.other_willreceiv,a.prepayment,a.dividend_willreceiv,a.interest_willreceiv,a.inventories, \
a.amor_exp,a.notcash_within_1y,a.sett_rsrv,a.loanto_oth_bank_fi,a.premium_receiv, \
a.reinsur_receiv,a.reinsur_res_receiv,a.pur_resale_fa,a.oth_cur_assets,a.total_cur_assets, \
a.fa_avail_for_sale,a.htm_invest,a.long_stock_invest,a.invest_real_estate,a.time_deposits, \
a.oth_assets,a.long_term_rec,a.fix_assets,a.constr_in_process,a.const_materials, \
a.fixed_assets_disp,a.produc_bio_assets,a.oil_and_gas_assets,a.intan_assets,a.study_spending, \
a.goodwill,a.long_term_amor_exp,a.defer_tax_assets,a.decr_in_disbur,a.other_not_cash, \
a.total_not_cash,a.cash_reser_cb,a.depos_in_oth_bfi,a.prec_metals,a.deriv_assets, \
a.rr_reins_une_prem,a.rr_reins_outstd_cla,a.rr_reins_lins_liab,a.rr_reins_lthins_liab,a.refund_depos, \
a.ph_pledge_loans,a.refund_cap_depos,a.indep_acct_assets,a.client_depos,a.client_prov, \
a.transac_seat_fee,a.invest_as_receiv,a.total_assets,a.long_borrow,a.short_borrow, \
a.central_bank_borrow,a.depos_ib_deposits,a.loan_oth_bank,a.trading_finance_load,a.notes_payable, \
a.acct_payable,a.adv_receipts,a.sold_for_repur_fa,a.comm_payable,a.payroll_payable, \
a.taxes_payable,a.interst_payable,a.dividend_payable,a.oth_payable,a.acc_exp, \
a.deferred_inc,a.st_bonds_payable,a.payable_to_reinsurer,a.rsrv_insur_cont,a.acting_trading_sec, \
a.acting_uw_sec,a.non_cur_liab_due_1y,a.oth_cur_liab,a.total_cur_liab,a.bond_payable, \
a.long_money_payable,a.specific_payables,a.estimated_liab,a.defer_tax_liab,a.defer_inc_non_cur_liab, \
a.other_not_cur_load,a.total_not_cur_load,a.depos_oth_bfi,a.deriv_liab,a.depos, \
a.agency_bus_liab,a.oth_liab,a.prem_receiv_adva,a.depos_received,a.ph_invest, \
a.reser_une_prem,a.reser_outstd_claims,a.reser_lins_liab,a.reser_lthins_liab,a.indept_acc_liab, \
a.pledge_borr,a.indem_payable,a.policy_div_payable,a.total_liab,a.treasury_share, \
a.ordin_risk_reser,a.forex_differ,a.invest_loss_unconf,a.minority_int,a.total_hldr_eqy_exc_min_int, \
a.total_hldr_eqy_inc_min_int,a.total_liab_hldr_eqy,a.lt_payroll_payable,a.oth_comp_income,a.oth_eqt_tools, \
a.oth_eqt_tools_p_shr,a.lending_funds,a.acc_receivable,a.st_fin_payable,a.payables, \
a.hfs_assets,a.hfs_sales,a.update_flag \
  FROM (SELECT a.* \
	  FROM company_balance_sheet a \
	 WHERE a.product_code = '%s' \
	   AND a.report_date %%10000 = 1231 \
	UNION \
	SELECT a.* \
	  FROM company_balance_sheet a, \
	       (SELECT MAX(a.report_date) maxreportdate \
		  FROM company_balance_sheet a \
		 WHERE a.product_code = '%s') b \
	 WHERE a.product_code = '%s' \
	   AND a.report_date = b.maxreportdate) a \
  ORDER BY a.report_date DESC \
  LIMIT %d"

COMPANYFINANCE_PUBYEARSELECTSQL = {"company_income":INCOME_PUBYEARSELECTSQL,
                                   "company_cashflow": CASHFLOW_PUBYEARSELECTSQL,
                                   "company_balance_sheet": BALACESHEET_PUBYEARSELECTSQL}

INCOME_PUBQUARTSELECTSQL = "SELECT a.product_code,a.announce_date,a.f_announce_date,a.report_type,a.report_date,\
a.company_type,a.basic_eps,a.diluted_eps,a.total_revenue,a.revenue,\
a.int_income,a.prem_earned,a.comm_income,a.n_commis_income,a.n_oth_income,\
a.n_oth_b_income,a.prem_income,a.out_prem,a.une_prem_reser,a.reins_income,\
a.n_sec_tb_income,a.n_sec_uw_income,a.n_asset_mg_income,a.oth_b_income,a.fv_value_chg_gain,\
a.invest_income,a.ass_invest_income,a.forex_gain,a.total_cogs,a.oper_cost,\
a.int_exp,a.comm_exp,a.biz_tax_surchg,a.sell_exp,a.admin_exp,\
a.fin_exp,a.assets_impair_loss,a.prem_refund,a.compens_payout,a.reser_insur_liab,\
a.div_payt,a.reins_exp,a.oper_exp,a.compens_payout_refu,a.insur_reser_refu,\
a.reins_cost_refund,a.other_bus_cost,a.operate_profit,a.non_oper_income,a.non_oper_exp,\
a.nca_disploss,a.total_profit,a.income_tax,a.n_income,a.n_income_attr_p,\
a.minority_gain,a.oth_compr_income,a.t_compr_income,a.compr_inc_attr_p,a.compr_inc_attr_m_s, \
a.ebit,a.ebitda,a.insurance_exp,a.undist_profit,a.distable_profit,\
a.update_flag \
FROM (SELECT a.* \
	  FROM company_income a, \
	       (SELECT MAX(a.report_date) maxreportdate \
		      FROM company_income a \
		     WHERE a.product_code = '%s') b \
	 WHERE a.product_code = '%s' \
	   AND a.report_date%%10000 = b.maxreportdate%%10000) a \
  ORDER BY a.report_date DESC \
  LIMIT %d"
CASHFLOW_PUBQUARTSELECTSQL = "SELECT a.product_code,a.announce_date,a.f_announce_date,a.report_date,a.report_type, \
a.company_type,a.net_profit,a.finan_exp,a.c_fr_sale_sg,a.recp_tax_rends, \
a.n_depos_incr_fi,a.n_incr_loans_cb,a.n_inc_borr_oth_fi,a.prem_fr_orig_contr,a.n_incr_insured_dep, \
a.n_reinsur_prem,a.n_incr_disp_tfa,a.ifc_cash_incr,a.n_incr_disp_faas,a.n_incr_loans_oth_bank, \
a.n_cap_incr_repur,a.c_fr_oth_operate_a,a.c_inf_fr_operate_a,a.c_paid_goods_s,a.c_paid_to_for_empl, \
a.c_paid_for_taxes,a.n_incr_clt_loan_adv,a.n_incr_dep_cbob,a.c_pay_claims_orig_inco,a.pay_handling_chrg, \
a.pay_comm_insur_plcy,a.oth_cash_pay_oper_act,a.st_cash_out_act,a.n_cashflow_act,a.oth_recp_ral_inv_act, \
a.c_disp_withdrwl_invest,a.c_recp_return_invest,a.n_recp_disp_fiolta,a.n_recp_disp_sobu,a.stot_inflows_inv_act, \
a.c_pay_acq_const_fiolta,a.c_paid_invest,a.n_disp_subs_oth_biz,a.oth_pay_ral_inv_act,a.n_incr_pledge_loan, \
a.stot_out_inv_act,a.n_cashflow_inv_act,a.c_recp_borrow,a.proc_issue_bonds,a.oth_cash_recp_ral_fnc_act, \
a.stot_cash_in_fnc_act,a.free_cashflow,a.c_prepay_amt_borr,a.c_pay_dist_dpcp_int_exp,a.incl_dvd_profit_paid_sc_ms, \
a.oth_cashpay_ral_fnc_act,a.stot_cashout_fnc_act,a.n_cash_flows_fnc_act,a.eff_fx_flu_cash,a.n_incr_cash_cash_equ, \
a.c_cash_equ_beg_period,a.c_cash_equ_end_period,a.c_recp_cap_contrib,a.incl_cash_rec_saims,a.uncon_invest_loss, \
a.prov_depr_assets,a.depr_fa_coga_dpba,a.amort_intang_assets,a.lt_amort_deferred_exp,a.decr_deferred_exp, \
a.incr_acc_exp,a.loss_disp_fiolta,a.loss_scr_fa,a.loss_fv_chg,a.invest_loss, \
a.decr_def_inc_tax_assets,a.incr_def_inc_tax_liab,a.decr_inventories,a.decr_oper_payable,a.incr_oper_payable, \
a.others_payable,a.conv_debt_into_cap,a.conv_copbonds_due_within_1y,a.fa_fnc_leases,a.end_bal_cash, \
a.beg_bal_cash,a.end_bal_cash_equ,a.beg_bal_cash_equ,a.im_n_incr_cash_equ,a.update_flag \
  FROM (SELECT a.* \
          FROM company_cashflow a, \
               (SELECT MAX(a.report_date) maxreportdate \
              FROM company_balance_sheet a \
             WHERE a.product_code = '%s') b \
         WHERE a.product_code = '%s' \
           AND a.report_date%%10000 = b.maxreportdate%%10000) a \
  ORDER BY a.report_date DESC \
  LIMIT %d"
BALACESHEET_PUBQUARTSELECTSQL = "SELECT a.product_code,a.announce_date,a.f_announce_date,a.report_date,a.report_type, \
a.company_type,a.total_share,a.cap_rese,a.undistr_profit,a.surplus_rese, \
a.special_rese,a.money_cap,a.trade_asset,a.notes_willreceiv,a.accounts_willreceiv, \
a.other_willreceiv,a.prepayment,a.dividend_willreceiv,a.interest_willreceiv,a.inventories, \
a.amor_exp,a.notcash_within_1y,a.sett_rsrv,a.loanto_oth_bank_fi,a.premium_receiv, \
a.reinsur_receiv,a.reinsur_res_receiv,a.pur_resale_fa,a.oth_cur_assets,a.total_cur_assets, \
a.fa_avail_for_sale,a.htm_invest,a.long_stock_invest,a.invest_real_estate,a.time_deposits, \
a.oth_assets,a.long_term_rec,a.fix_assets,a.constr_in_process,a.const_materials, \
a.fixed_assets_disp,a.produc_bio_assets,a.oil_and_gas_assets,a.intan_assets,a.study_spending, \
a.goodwill,a.long_term_amor_exp,a.defer_tax_assets,a.decr_in_disbur,a.other_not_cash, \
a.total_not_cash,a.cash_reser_cb,a.depos_in_oth_bfi,a.prec_metals,a.deriv_assets, \
a.rr_reins_une_prem,a.rr_reins_outstd_cla,a.rr_reins_lins_liab,a.rr_reins_lthins_liab,a.refund_depos, \
a.ph_pledge_loans,a.refund_cap_depos,a.indep_acct_assets,a.client_depos,a.client_prov, \
a.transac_seat_fee,a.invest_as_receiv,a.total_assets,a.long_borrow,a.short_borrow, \
a.central_bank_borrow,a.depos_ib_deposits,a.loan_oth_bank,a.trading_finance_load,a.notes_payable, \
a.acct_payable,a.adv_receipts,a.sold_for_repur_fa,a.comm_payable,a.payroll_payable, \
a.taxes_payable,a.interst_payable,a.dividend_payable,a.oth_payable,a.acc_exp, \
a.deferred_inc,a.st_bonds_payable,a.payable_to_reinsurer,a.rsrv_insur_cont,a.acting_trading_sec, \
a.acting_uw_sec,a.non_cur_liab_due_1y,a.oth_cur_liab,a.total_cur_liab,a.bond_payable, \
a.long_money_payable,a.specific_payables,a.estimated_liab,a.defer_tax_liab,a.defer_inc_non_cur_liab, \
a.other_not_cur_load,a.total_not_cur_load,a.depos_oth_bfi,a.deriv_liab,a.depos, \
a.agency_bus_liab,a.oth_liab,a.prem_receiv_adva,a.depos_received,a.ph_invest, \
a.reser_une_prem,a.reser_outstd_claims,a.reser_lins_liab,a.reser_lthins_liab,a.indept_acc_liab, \
a.pledge_borr,a.indem_payable,a.policy_div_payable,a.total_liab,a.treasury_share, \
a.ordin_risk_reser,a.forex_differ,a.invest_loss_unconf,a.minority_int,a.total_hldr_eqy_exc_min_int, \
a.total_hldr_eqy_inc_min_int,a.total_liab_hldr_eqy,a.lt_payroll_payable,a.oth_comp_income,a.oth_eqt_tools, \
a.oth_eqt_tools_p_shr,a.lending_funds,a.acc_receivable,a.st_fin_payable,a.payables, \
a.hfs_assets,a.hfs_sales,a.update_flag \
  FROM (SELECT a.* \
	  FROM company_balance_sheet a, \
	       (SELECT MAX(a.report_date) maxreportdate \
		  FROM company_balance_sheet a \
		 WHERE a.product_code = '%s') b \
	 WHERE a.product_code = '%s' \
	   AND a.report_date%%10000 = b.maxreportdate%%10000) a \
  ORDER BY a.report_date DESC \
  LIMIT %d"

COMPANYFINANCE_PUBQUARTSELECTSQL = {"company_income":INCOME_PUBQUARTSELECTSQL,
                                   "company_cashflow": CASHFLOW_PUBQUARTSELECTSQL,
                                   "company_balance_sheet": BALACESHEET_PUBQUARTSELECTSQL}
# 公司相关的会计数据 end

# datadownloadlog 日志文件begin
DATADOWNLOG_GETDATA="select product_code,eventtype,dealstatus,sourcetype,logdate,logtime from datadownloadlog where product_code='%s' and eventtype='%s' and sourcetype='%s' and logdate=%d "
DATADOWNLOG_INSERTDATA="INSERT INTO datadownloadlog(product_code,eventtype,dealstatus,sourcetype,logdate,logtime) VALUES ('%s','%s','%s','%s',%d,%d)"
DATADOWNLOG_UPDATEDATA="update datadownloadlog set dealstatus='%s' where product_code='%s' and eventtype='%s' and sourcetype='%s' and logdate=%d"
# datadownloadlog 日志文件end

# 通达信数据插入日线数据库语句 begin
TDXDATAINSERTDATABASE="INSERT INTO producttradedata(product_code, trade_date,open_price,high_price,close_price,low_price,product_volume,product_amount)\
        VALUES('%s',%d,%f,%f,%f,%f,%f,%f)"
# 通达信数据插入日线数据库语句 end
# 通达信数据插入30min线数据库语句 begin
TDX30DATAINSERTDATABASE="INSERT INTO prod30tradedata(product_code,symbol_code, trade_date,trade_time,open_price,high_price,close_price,low_price,product_volume,product_amount)\
        VALUES('%s','%s',%d,%d,%f,%f,%f,%f,%f,%f)"
CSV30DATAINSERTDB = "INSERT INTO prod30tradedata(product_code,symbol_code, trade_date,trade_time,open_price,high_price,close_price,low_price,product_volume,product_amount) VALUES"
CSV30INSERTVAR = "('%s','%s',%d,%d,%f,%f,%f,%f,%f,%f),"
# 通达信数据插入30min线数据库语句 end

# 日交易数据获取 begin
DAYTRADEDATA_GET="select product_code, trade_date,open_price,high_price,close_price,low_price,product_volume,product_amount from \
 producttradedata where product_code = '%s' and trade_date > %d order by trade_date "
DAYTRADEDATA_ONEDATEGET="select product_code, trade_date,open_price,high_price,close_price,low_price,product_volume,product_amount from \
 producttradedata where product_code = '%s' and trade_date = %d "
# 日交易数据获取 end

# 日交易包含关系处理后的数据插入 begin
ENTDAYTRADEDATA_INSERT = "INSERT INTO %s (product_code, trade_date,open_price,high_price,close_price,low_price,merge_flag,updown_flag, trade_time) VALUES"
ENTDAYTRADEDATA_INSERTDATA = "('%s',%d,%f,%f,%f,%f,'%s','%s', %d),"
# 日交易包含关系处理后的数据插入 end

# 日entdaytradedata表中数据获取 begin
ENTDAYTRADEDATA_GET="select product_code, trade_date,open_price,high_price,close_price,low_price,merge_flag,updown_flag,trade_time from %s a where a.product_code = '%s' and a.trade_date >= %d and a.trade_time >= %d order by a.trade_date,a.trade_time "
ENTDAYTRADEDATA_UPDATETBL = "update %s "
ENTDAYTRADEDATA_UPDATEUUPDOWNFLAG = "set updown_flag = %s where product_code = %s and trade_date = %s"
ENTDAYTRADEDATA_REALUPDATEUUPDOWNFLAG = "update %s set updown_flag = '%s' where product_code = '%s' and trade_date = %s"
ENTDAYTRADEDATA_ABTYPINGGET="select product_code, trade_date,open_price,high_price,close_price,low_price,merge_flag,updown_flag,trade_time from %s a \
 where a.product_code = '%s' and a.trade_date >= %d and updown_flag in ('A','B') and a.trade_time >= %d order by a.trade_date,a.trade_time "
ENTDAYTRADEDATA_MAXTRADEDATEGET="select ifnull(max(trade_date),0) maxtradedate from %s a where a.product_code = '%s' "
# 最近A或者B交易日获取
ENTDAYTRADEDATA_LASTAORBDATEGET = "select ifnull(max(trade_date),0) maxtradedate from %s a where a.product_code = '%s' and a.updown_flag IN ('A','B')"
# 日entdaytradedata表中数据获取 end

