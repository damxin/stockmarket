-- CREATE DATABASE IF NOT EXISTS stockmarket;
-- GRANT ALL ON stockmarket.* to 'root'@'%' IDENTIFIED BY 'root';
-- GRANT ALL ON stockmarket.* to 'root'@'127.0.0.1' IDENTIFIED BY 'root';
-- GRANT ALL ON stockmarket.* to 'root'@'localhost' IDENTIFIED BY 'root';
-- GRANT SELECT ON mysql.help_topic TO 'root'@'%' IDENTIFIED BY 'root';
-- GRANT PROCESS,FILE,SUPER,REPLICATION CLIENT,REPLICATION SLAVE  ON *.* to 'root'@'%' IDENTIFIED BY 'root';
-- GRANT PROCESS,FILE,SUPER,REPLICATION CLIENT,REPLICATION SLAVE  ON *.* to 'root'@'127.0.0.1' IDENTIFIED BY 'root';
-- GRANT PROCESS,FILE,SUPER,REPLICATION CLIENT,REPLICATION SLAVE  ON *.* to 'root'@'localhost' IDENTIFIED BY 'root';

DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='productdatabaserule'; 
            IF v_rowcount = 0 THEN
                CREATE TABLE productdatabaserule
                (
                min_product_code VARCHAR(10),
                max_product_code VARCHAR(10),
                min_trade_date int(8),
                max_trade_date int(8),
                logic_name VARCHAR(20),
                pooltype CHAR(1), -- 0:主库 1:分库
                work_flag CHAR(1) -- 启用标志
                );
                END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 

-- insert into productdatabaserule(min_product_code,max_product_code,logic_name,pooltype,work_flag) values("******","******","dbbase",0,1),("000000","299999","trade1",1,1),("300000","599999","trade2",0,1),("600000","999999","trade3",0,1)

DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='productbasicinfo'; 
            IF v_rowcount = 0 THEN 
            create table productbasicinfo
            (
              product_code varchar(10),
              product_name varchar(30),
              product_type char(1),
              money_type char(1),
              product_area varchar(20),
              product_industry varchar(40),
              product_fullname varchar(120),
              market_type varchar(1),
              exchange_code varchar(10),
              ipo_status varchar(1),
              listed_date int(8),
              delisted_date int(8),
              primary key (product_code)
            );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 


DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='poolinfo'; 
            IF v_rowcount = 0 THEN 
                create table poolinfo
                (
                  product_code_min varchar(10),
                  product_code_max varchar(10),
                  trade_day_min int(8),
                  trade_day_max int(8),
                  db_logicname varchar(10),
                  db_flag char(1)
                );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;
 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='openday'; 
            IF v_rowcount = 0 THEN 
                create table openday
                (
                  exchange_code varchar(10),
                  trade_date int(8),
                  trade_flag varchar(1),
                  pretrade_day int(8),
                  primary key (exchange_code, trade_date)
                );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;
 
DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='exchangeinfo'; 
            IF v_rowcount = 0 THEN 
                create table exchangeinfo
                (
                  exchange_code varchar(10),
                  exchange_name varchar(60),
                  country_code varchar(20),
                  primary key (exchange_code)
                );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;
 
DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='company_balance_sheet'; 
            IF v_rowcount = 0 THEN 
                create table company_balance_sheet
                (
                  product_code varchar(10),
                  announce_date int(8),
                  f_announce_date int(8),
                  report_date int(8),
                  report_type varchar(20),
                  company_type varchar(16),
                  total_share decimal(16,2),
                  cap_rese decimal(16,2),
                  undistr_profit decimal(16,2),
                  surplus_rese decimal(16,2),
                  special_rese decimal(16,2),
                  money_cap decimal(16,2),
                  trade_asset decimal(16,2),
                  notes_willreceiv decimal(16,2),
                  accounts_willreceiv decimal(16,2),
                  other_willreceiv decimal(16,2),
                  prepayment decimal(16,2),
                  dividend_willreceiv decimal(16,2),
                  interest_willreceiv decimal(16,2),
                  inventories decimal(16,2),
                  amor_exp decimal(16,2),
                  notcash_within_1y decimal(16,2),
                  sett_rsrv decimal(16,2),
                  loanto_oth_bank_fi decimal(16,2),
                  premium_receiv decimal(16,2),
                  reinsur_receiv decimal(16,2),
                  reinsur_res_receiv decimal(16,2),
                  pur_resale_fa decimal(16,2),
                  oth_cur_assets decimal(16,2),
                  total_cur_assets decimal(16,2),
                  fa_avail_for_sale decimal(16,2),
                  htm_invest decimal(16,2),
                  long_stock_invest decimal(16,2),
                  invest_real_estate decimal(16,2),
                  time_deposits decimal(16,2),
                  oth_assets decimal(16,2),
                  long_term_rec decimal(16,2),
                  fix_assets decimal(16,2),
                  constr_in_process decimal(16,2),
                  const_materials decimal(16,2),
                  fixed_assets_disp decimal(16,2),
                  produc_bio_assets decimal(16,2),
                  oil_and_gas_assets decimal(16,2),
                  intan_assets decimal(16,2),
                  study_spending decimal(16,2),
                  goodwill decimal(16,2),
                  long_term_amor_exp decimal(16,2),
                  defer_tax_assets decimal(16,2),
                  decr_in_disbur decimal(16,2),
                  other_not_cash decimal(16,2),
                  total_not_cash decimal(16,2),
                  cash_reser_cb decimal(16,2),
                  depos_in_oth_bfi decimal(16,2),
                  prec_metals decimal(16,2),
                  deriv_assets decimal(16,2),
                  rr_reins_une_prem decimal(16,2),
                  rr_reins_outstd_cla decimal(16,2),
                  rr_reins_lins_liab decimal(16,2),
                  rr_reins_lthins_liab decimal(16,2),
                  refund_depos decimal(16,2),
                  ph_pledge_loans decimal(16,2),
                  refund_cap_depos decimal(16,2),
                  indep_acct_assets decimal(16,2),
                  client_depos decimal(16,2),
                  client_prov decimal(16,2),
                  transac_seat_fee decimal(16,2),
                  invest_as_receiv decimal(16,2),
                  total_assets decimal(16,2),
                  long_borrow decimal(16,2),
                  short_borrow decimal(16,2),
                  central_bank_borrow decimal(16,2),
                  depos_ib_deposits decimal(16,2),
                  loan_oth_bank decimal(16,2),
                  trading_finance_load decimal(16,2),
                  notes_payable decimal(16,2),
                  acct_payable decimal(16,2),
                  adv_receipts decimal(16,2),
                  sold_for_repur_fa decimal(16,2),
                  comm_payable decimal(16,2),
                  payroll_payable decimal(16,2),
                  taxes_payable decimal(16,2),
                  interst_payable decimal(16,2),
                  dividend_payable decimal(16,2),
                  oth_payable decimal(16,2),
                  acc_exp decimal(16,2),
                  deferred_inc decimal(16,2),
                  st_bonds_payable decimal(16,2),
                  payable_to_reinsurer decimal(16,2),
                  rsrv_insur_cont decimal(16,2),
                  acting_trading_sec decimal(16,2),
                  acting_uw_sec decimal(16,2),
                  non_cur_liab_due_1y decimal(16,2),
                  oth_cur_liab decimal(16,2),
                  total_cur_liab decimal(16,2),
                  bond_payable decimal(16,2),
                  long_money_payable decimal(16,2),
                  specific_payables decimal(16,2),
                  estimated_liab decimal(16,2),
                  defer_tax_liab decimal(16,2),
                  defer_inc_non_cur_liab decimal(16,2),
                  other_not_cur_load decimal(16,2),
                  total_not_cur_load decimal(16,2),
                  depos_oth_bfi decimal(16,2),
                  deriv_liab decimal(16,2),
                  depos decimal(16,2),
                  agency_bus_liab decimal(16,2),
                  oth_liab decimal(16,2),
                  prem_receiv_adva decimal(16,2),
                  depos_received decimal(16,2),
                  ph_invest decimal(16,2),
                  reser_une_prem decimal(16,2),
                  reser_outstd_claims decimal(16,2),
                  reser_lins_liab decimal(16,2),
                  reser_lthins_liab decimal(16,2),
                  indept_acc_liab decimal(16,2),
                  pledge_borr decimal(16,2),
                  indem_payable decimal(16,2),
                  policy_div_payable decimal(16,2),
                  total_liab decimal(16,2),
                  treasury_share decimal(16,2),
                  ordin_risk_reser decimal(16,2),
                  forex_differ decimal(16,2),
                  invest_loss_unconf decimal(16,2),
                  minority_int decimal(16,2),
                  total_hldr_eqy_exc_min_int decimal(16,2),
                  total_hldr_eqy_inc_min_int decimal(16,2),
                  total_liab_hldr_eqy decimal(16,2),
                  lt_payroll_payable decimal(16,2),
                  oth_comp_income decimal(16,2),
                  oth_eqt_tools decimal(16,2),
                  oth_eqt_tools_p_shr decimal(16,2),
                  lending_funds decimal(16,2),
                  acc_receivable decimal(16,2),
                  st_fin_payable decimal(16,2),
                  payables decimal(16,2),
                  hfs_assets decimal(16,2),
                  hfs_sales decimal(16,2),
                  update_flag char(1)
                );
                ALTER TABLE company_balance_sheet ADD INDEX idx_balance_sheet (product_code,report_date);
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;
 
DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='company_cashflow'; 
            IF v_rowcount = 0 THEN 
                create table company_cashflow
                (
                  product_code varchar(10),
                  announce_date int(8),
                  f_announce_date int(8),
                  report_date int(8),
                  report_type varchar(20),
                  company_type varchar(16),
                  net_profit decimal(16,2),
                  finan_exp decimal(16,2),
                  c_fr_sale_sg decimal(16,2),
                  recp_tax_rends decimal(16,2),
                  n_depos_incr_fi decimal(16,2),
                  n_incr_loans_cb decimal(16,2),
                  n_inc_borr_oth_fi decimal(16,2),
                  prem_fr_orig_contr decimal(16,2),
                  n_incr_insured_dep decimal(16,2),
                  n_reinsur_prem decimal(16,2),
                  n_incr_disp_tfa decimal(16,2),
                  ifc_cash_incr decimal(16,2),
                  n_incr_disp_faas decimal(16,2),
                  n_incr_loans_oth_bank decimal(16,2),
                  n_cap_incr_repur decimal(16,2),
                  c_fr_oth_operate_a decimal(16,2),
                  c_inf_fr_operate_a decimal(16,2),
                  c_paid_goods_s decimal(16,2),
                  c_paid_to_for_empl decimal(16,2),
                  c_paid_for_taxes decimal(16,2),
                  n_incr_clt_loan_adv decimal(16,2),
                  n_incr_dep_cbob decimal(16,2),
                  c_pay_claims_orig_inco decimal(16,2),
                  pay_handling_chrg decimal(16,2),
                  pay_comm_insur_plcy decimal(16,2),
                  oth_cash_pay_oper_act decimal(16,2),
                  st_cash_out_act decimal(16,2),
                  n_cashflow_act decimal(16,2),
                  oth_recp_ral_inv_act decimal(16,2),
                  c_disp_withdrwl_invest decimal(16,2),
                  c_recp_return_invest decimal(16,2),
                  n_recp_disp_fiolta decimal(16,2),
                  n_recp_disp_sobu decimal(16,2),
                  stot_inflows_inv_act decimal(16,2),
                  c_pay_acq_const_fiolta decimal(16,2),
                  c_paid_invest decimal(16,2),
                  n_disp_subs_oth_biz decimal(16,2),
                  oth_pay_ral_inv_act decimal(16,2),
                  n_incr_pledge_loan decimal(16,2),
                  stot_out_inv_act decimal(16,2),
                  n_cashflow_inv_act decimal(16,2),
                  c_recp_borrow decimal(16,2),
                  proc_issue_bonds decimal(16,2),
                  oth_cash_recp_ral_fnc_act decimal(16,2),
                  stot_cash_in_fnc_act decimal(16,2),
                  free_cashflow decimal(16,2),
                  c_prepay_amt_borr decimal(16,2),
                  c_pay_dist_dpcp_int_exp decimal(16,2),
                  incl_dvd_profit_paid_sc_ms decimal(16,2),
                  oth_cashpay_ral_fnc_act decimal(16,2),
                  stot_cashout_fnc_act decimal(16,2),
                  n_cash_flows_fnc_act decimal(16,2),
                  eff_fx_flu_cash decimal(16,2),
                  n_incr_cash_cash_equ decimal(16,2),
                  c_cash_equ_beg_period decimal(16,2),
                  c_cash_equ_end_period decimal(16,2),
                  c_recp_cap_contrib decimal(16,2),
                  incl_cash_rec_saims decimal(16,2),
                  uncon_invest_loss decimal(16,2),
                  prov_depr_assets decimal(16,2),
                  depr_fa_coga_dpba decimal(16,2),
                  amort_intang_assets decimal(16,2),
                  lt_amort_deferred_exp decimal(16,2),
                  decr_deferred_exp decimal(16,2),
                  incr_acc_exp decimal(16,2),
                  loss_disp_fiolta decimal(16,2),
                  loss_scr_fa decimal(16,2),
                  loss_fv_chg decimal(16,2),
                  invest_loss decimal(16,2),
                  decr_def_inc_tax_assets decimal(16,2),
                  incr_def_inc_tax_liab decimal(16,2),
                  decr_inventories decimal(16,2),
                  decr_oper_payable decimal(16,2),
                  incr_oper_payable decimal(16,2),
                  others_payable decimal(16,2),
                  conv_debt_into_cap decimal(16,2),
                  conv_copbonds_due_within_1y decimal(16,2),
                  fa_fnc_leases decimal(16,2),
                  end_bal_cash decimal(16,2),
                  beg_bal_cash decimal(16,2),
                  end_bal_cash_equ decimal(16,2),
                  beg_bal_cash_equ decimal(16,2),
                  im_n_incr_cash_equ decimal(16,2),
                  update_flag char(1)
                );
                ALTER TABLE company_cashflow ADD INDEX idx_cashflow (product_code,report_date);
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;
 
DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='company_income'; 
            IF v_rowcount = 0 THEN 
                create table company_income
                (
                  product_code varchar(10),
                  announce_date int(8),
                  f_announce_date int(8),
                  report_type varchar(20),
                  report_date int(8),
                  company_type varchar(16),
                  basic_eps decimal(16,2),
                  diluted_eps decimal(16,2),
                  total_revenue decimal(16,2),
                  revenue decimal(16,2),
                  int_income decimal(16,2),
                  prem_earned decimal(16,2),
                  comm_income decimal(16,2),
                  n_commis_income decimal(16,2),
                  n_oth_income decimal(16,2),
                  n_oth_b_income decimal(16,2),
                  prem_income decimal(16,2),
                  out_prem decimal(16,2),
                  une_prem_reser decimal(16,2),
                  reins_income decimal(16,2),
                  n_sec_tb_income decimal(16,2),
                  n_sec_uw_income decimal(16,2),
                  n_asset_mg_income decimal(16,2),
                  oth_b_income decimal(16,2),
                  fv_value_chg_gain decimal(16,2),
                  invest_income decimal(16,2),
                  ass_invest_income decimal(16,2),
                  forex_gain decimal(16,2),
                  total_cogs decimal(16,2),
                  oper_cost decimal(16,2),
                  int_exp decimal(16,2),
                  comm_exp decimal(16,2),
                  biz_tax_surchg decimal(16,2),
                  sell_exp decimal(16,2),
                  admin_exp decimal(16,2),
                  fin_exp decimal(16,2),
                  assets_impair_loss decimal(16,2),
                  prem_refund decimal(16,2),
                  compens_payout decimal(16,2),
                  reser_insur_liab decimal(16,2),
                  div_payt decimal(16,2),
                  reins_exp decimal(16,2),
                  oper_exp decimal(16,2),
                  compens_payout_refu decimal(16,2),
                  insur_reser_refu decimal(16,2),
                  reins_cost_refund decimal(16,2),
                  other_bus_cost decimal(16,2),
                  operate_profit decimal(16,2),
                  non_oper_income decimal(16,2),
                  non_oper_exp decimal(16,2),
                  nca_disploss decimal(16,2),
                  total_profit decimal(16,2),
                  income_tax decimal(16,2),
                  n_income decimal(16,2),
                  n_income_attr_p decimal(16,2),
                  minority_gain decimal(16,2),
                  oth_compr_income decimal(16,2),
                  t_compr_income decimal(16,2),
                  compr_inc_attr_p decimal(16,2),
                  compr_inc_attr_m_s decimal(16,2),
                  ebit decimal(16,2),
                  ebitda decimal(16,2),
                  insurance_exp decimal(16,2),
                  undist_profit decimal(16,2),
                  distable_profit decimal(16,2),
                  update_flag char(1)
                );
                ALTER TABLE company_income ADD INDEX idx_income (product_code,report_date);
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;
 
DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='productdailybasicinfo'; 
            IF v_rowcount = 0 THEN 
                create table productdailybasicinfo
                (
                  product_code varchar(10),
                  trade_date int(8),
                  close_price decimal(16,2),
                  turnover_rate decimal(9,8),
                  turnover_rate_f decimal(9,8),
                  product_volume decimal(16,2),
                  volume_ratio decimal(11,8),
                  pe_static decimal(6,2),
                  pe_ttm decimal(6,2),
                  stock_pb decimal(6,2),
                  ps_static decimal(6,2),
                  ps_ttm decimal(6,2),
                  total_share decimal(16,2),
                  float_share decimal(16,2),
                  free_share decimal(16,2),
                  total_mv decimal(16,2),
                  cicr_mv decimal(16,2),
                  primary key (product_code, trade_date)
                );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;

DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='producttradedata'; 
            IF v_rowcount = 0 THEN 
                create table producttradedata
                (
                  product_code varchar(10),
                  trade_date int(8),
                  open_price decimal(16,2),
                  high_price decimal(16,2),
                  close_price decimal(16,2),
                  low_price decimal(16,2),
                  product_volume decimal(16,2),
                  product_amount decimal(16,2),
                  primary key (product_code, trade_date)
                );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;


DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='tfilefielddict'; 
            IF v_rowcount = 0 THEN 
                create table tfilefielddict
                (
                  filechiname varchar(60),
                  l_fileid int(4)
                );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;

DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='tstfielddict'; 
            IF v_rowcount = 0 THEN 
                create table tstfielddict
                (
                  dbengname varchar(30),
                  l_stid int(4)
                );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;

DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='tfilestfield'; 
            IF v_rowcount = 0 THEN 
                create table tfilestfield
                (
                  l_fileid int(4),
                  l_stid int(4),
                  filetype varchar(2)
                );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;

DROP PROCEDURE IF EXISTS sp_db_mysql; 
DELIMITER $$ 
    CREATE PROCEDURE sp_db_mysql() 
        BEGIN 
            DECLARE v_rowcount INT; 
            DECLARE database_name VARCHAR(100); 
            SELECT DATABASE() INTO database_name; 
            SELECT COUNT(1) INTO v_rowcount FROM information_schema.tables WHERE table_schema= database_name AND table_name='datadownloadlog'; 
            IF v_rowcount = 0 THEN 
                create table datadownloadlog
                (
                  product_code varchar(10),
                  eventtype varchar(1),
                  dealstatus varchar(1),
                  sourcetype varchar(1),
                  logdate int(8),
                  logtime int(6)
                );
            END IF; 
    END$$ 
DELIMITER; 
CALL sp_db_mysql(); 
DROP PROCEDURE IF EXISTS sp_db_mysql;

 
