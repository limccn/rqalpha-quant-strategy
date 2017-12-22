create table FI_QUOTE_DAILY_SZ000001
(
DATE_TIME String comment '日期',
STOCK_CODE String comment '股票代码',
STOCK_NAME String comment '名称',
CLOSE_PRICE DECIMAL(12,4) comment '收盘价',
HIGH_PRICE DECIMAL(12,4) comment '最高价',
LOW_PRICE DECIMAL(12,4) comment '最低价',
OPEN_PRICE DECIMAL(12,4) comment '开盘价',
LAST_CLOSE_PRICE DECIMAL(12,4) comment '前收盘',
CHANGE DECIMAL(12,4) comment '涨跌额',
CHANGE_RATE DECIMAL(12,4) comment '涨跌幅',
TURNOVER_RATE DECIMAL(12,4) comment '换手率',
VOLUME DECIMAL(12,0) comment '成交量',
AMOUNT DECIMAL(16,4) comment '成交金额',
TOTAL_MARKET_CAP DECIMAL(16,4) comment '总市值',
FA_MARKET_CAP DECIMAL(16,4) comment '流通市值',
TURNOVER DECIMAL(12,0) comment '成交笔数'
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;