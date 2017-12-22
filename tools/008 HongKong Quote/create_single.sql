use ohs_stockdata_hk_test;

create table FI_QUOTE_DAILY_HKSE_STOCK_ALL
(
DATE_TIME String comment '日期',
OPEN_PRICE DECIMAL(12,4) comment '开盘价',
HIGH_PRICE DECIMAL(12,4) comment '最高价',
LOW_PRICE DECIMAL(12,4) comment '最低价',
CLOSE_PRICE DECIMAL(12,4) comment '收盘价',
VOLUME DECIMAL(12,0) comment '成交量',
OPEN_FLAG INT comment '开盘标志'
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;