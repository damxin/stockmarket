-- CREATE DATABASE IF NOT EXISTS stockmarket;
-- GRANT ALL ON stockmarket.* to 'root'@'%' IDENTIFIED BY 'root';
-- GRANT ALL ON stockmarket.* to 'root'@'127.0.0.1' IDENTIFIED BY 'root';
-- GRANT ALL ON stockmarket.* to 'root'@'localhost' IDENTIFIED BY 'root';
-- GRANT SELECT ON mysql.help_topic TO 'root'@'%' IDENTIFIED BY 'root';
-- GRANT PROCESS,FILE,SUPER,REPLICATION CLIENT,REPLICATION SLAVE  ON *.* to 'root'@'%' IDENTIFIED BY 'root';
-- GRANT PROCESS,FILE,SUPER,REPLICATION CLIENT,REPLICATION SLAVE  ON *.* to 'root'@'127.0.0.1' IDENTIFIED BY 'root';
-- GRANT PROCESS,FILE,SUPER,REPLICATION CLIENT,REPLICATION SLAVE  ON *.* to 'root'@'localhost' IDENTIFIED BY 'root';

-- DELIMITER $$
--     CREATE PROCEDURE sp_db_mysql()
--     BEGIN
--         DECLARE v_isexist INT;
--         SELECT COUNT(1) INTO v_isexist FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='ta_tfundconver_td' ;
--         IF v_isexist = 0 THEN
--         create table ta_tfundconver_td
--         (
--         	c_tenantid           varchar(20)    default ' '        not null,
--         	c_tacode             varchar(2)     default ' '        not null,
--         	c_fundcode           varchar(12)    default ' '        not null,
--         	c_othercode          varchar(12)    default ' '        not null,
--             c_databaseno         varchar(5)     default ' '        not null,
--             PRIMARY KEY(c_fundcode,c_othercode,c_databaseno,c_tacode,c_tenantid)
--         );
--     	end if;
--     END$$
-- DELIMITER;
-- 	call sp_db_mysql();
-- DROP PROCEDURE IF EXISTS sp_db_mysql;

-- DROP PROCEDURE IF EXISTS sp_db_mysql;
-- DELIMITER $$
--   CREATE PROCEDURE sp_db_mysql()
--     BEGIN
--         DECLARE v_isexist INT;
--         declare v_count INT;
--         SELECT COUNT(1) INTO v_isexist FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='ta_tlargeholdprofit' ;
--         IF v_isexist > 0 then
--             SELECT COUNT(1) INTO v_count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='ta_tlargeholdprofit' AND column_name = 'f_addshares' ;
--             if v_count = 0 then
--                 ALTER TABLE ta_tlargeholdprofit ADD f_addshares decimal(16,2) default 0;
--             end if;
--         end if;
--     END$$
-- DELIMITER ;
--   call sp_db_mysql();
-- DROP PROCEDURE IF EXISTS sp_db_mysql;

DELIMITER $$
    CREATE PROCEDURE sp_db_mysql()
    BEGIN
        DECLARE v_isexist INT;
        SELECT COUNT(1) INTO v_isexist FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='tstockinfo' ;
        IF v_isexist = 0 THEN
        create table tstockbasicinfo
        (
        	c_stockcode           varchar(10)    default ' '        not null,  -- 股票code
        	c_stockname           varchar(20)    default ' '        not null,  -- 股票名称
        	c_industry           varchar(12)    default ' '        not null,  -- 区域
        	d_ipodate            int(8)        default 0          not null,  -- 上市日期
            PRIMARY KEY(c_stockcode)
        );
    	end if;
    END$$
DELIMITER;
	call sp_db_mysql();
DROP PROCEDURE IF EXISTS sp_db_mysql;

DELIMITER $$
    CREATE PROCEDURE sp_db_mysql()
    BEGIN
        DECLARE v_isexist INT;
        SELECT COUNT(1) INTO v_isexist FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='tstockinfo' ;
        IF v_isexist = 0 THEN
        create table tstockbasicinfo
        (
        	c_stockcode           varchar(10)    default ' '        not null,  -- 股票code
        	c_stockname           varchar(20)    default ' '        not null,  -- 股票名称
        	c_industry           varchar(12)    default ' '        not null,  -- 区域
        	d_ipodate            int(8)        default 0          not null,  -- 上市日期
            PRIMARY KEY(c_stockcode)
        );
    	end if;
    END$$
DELIMITER;
	call sp_db_mysql();
DROP PROCEDURE IF EXISTS sp_db_mysql;