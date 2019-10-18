SELECT CONCAT("INSERT INTO stockmarket.producttradedata(product_code,trade_date,open_price,high_price, close_price, low_price, product_volume, product_amount) SELECT LEFT(a.ts_code,6) product_code,a.trade_date trade_date, a.open open_price,a.high high_price, a.close close_price, a.low low_price, a.vol product_volume,a.amount product_amount FROM stocknotdealmarket.",table_name," a WHERE NOT EXISTS (SELECT 1 FROM stockmarket.producttradedata b WHERE LEFT(a.ts_code,6) = b.product_code AND a.trade_date = b.trade_date);") 
FROM information_schema.tables a, stockmarket.productdatabaserule b 
WHERE table_schema = 'stocknotdealmarket' 
AND UPPER(a.table_name) <= UPPER(CONCAT("histtradedata",b.`max_product_code`))
AND UPPER(a.table_name) >= UPPER(CONCAT("histtradedata", b.`min_product_code`))
AND b.`pooltype` = 1
AND b.`work_flag` = 1
ORDER BY table_name;

SELECT CONCAT("INSERT INTO stocktrade1.producttradedata(product_code,trade_date,open_price,high_price, close_price, low_price, product_volume, product_amount) SELECT LEFT(a.ts_code,6) product_code,a.trade_date trade_date, a.open open_price,a.high high_price, a.close close_price, a.low low_price, a.vol product_volume,a.amount product_amount FROM stocknotdealmarket.",table_name," a WHERE NOT EXISTS (SELECT 1 FROM stocktrade1.producttradedata b WHERE LEFT(a.ts_code,6) = b.product_code AND a.trade_date = b.trade_date);") 
FROM information_schema.tables a, stocktrade1.productdatabaserule b 
WHERE table_schema = 'stocknotdealmarket' 
AND UPPER(a.table_name) <= UPPER(CONCAT("histtradedata",b.`max_product_code`))
AND UPPER(a.table_name) >= UPPER(CONCAT("histtradedata", b.`min_product_code`))
AND b.`pooltype` = 1
AND b.`work_flag` = 1
ORDER BY table_name;

SELECT CONCAT("INSERT INTO stocktrade2.producttradedata(product_code,trade_date,open_price,high_price, close_price, low_price, product_volume, product_amount) SELECT LEFT(a.ts_code,6) product_code,a.trade_date trade_date, a.open open_price,a.high high_price, a.close close_price, a.low low_price, a.vol product_volume,a.amount product_amount FROM stocknotdealmarket.",table_name," a WHERE NOT EXISTS (SELECT 1 FROM stocktrade2.producttradedata b WHERE LEFT(a.ts_code,6) = b.product_code AND a.trade_date = b.trade_date);") 
FROM information_schema.tables a, stocktrade2.productdatabaserule b 
WHERE table_schema = 'stocknotdealmarket' 
AND UPPER(a.table_name) <= UPPER(CONCAT("histtradedata",b.`max_product_code`))
AND UPPER(a.table_name) >= UPPER(CONCAT("histtradedata", b.`min_product_code`))
AND b.`pooltype` = 1
AND b.`work_flag` = 1
ORDER BY table_name;