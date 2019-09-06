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