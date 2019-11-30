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
             "company_income":LOGICNAME_TRADE,
             "histcastflow":LOGICNAME_TMPBASE,
             "company_cashflow":LOGICNAME_TRADE,
             "histbalance":LOGICNAME_TMPBASE,
             "company_balance_sheet":LOGICNAME_TRADE}

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
insurance_exp,undist_profit,distable_profit,'1' update_flag \
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
acc_receivable,st_fin_payable,payables,hfs_assets,hfs_sales,'1' update_flag \
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
end_bal_cash_equ, beg_bal_cash_equ, im_n_incr_cash_equ, '1' update_flag \
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
# 公司相关的会计数据 end