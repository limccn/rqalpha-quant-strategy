create table FI_QUOTE_DAILY_HKEX_
(
`DATE` String comment '日期',
OPEN DECIMAL(12,4) comment '开盘价',
HIGH DECIMAL(12,4) comment '最高价',
LOW DECIMAL(12,4) comment '最低价',
CLOSE DECIMAL(12,4) comment '收盘价',
VOLUME DECIMAL(12,4) comment '成交量',
OPEN_INT DECIMAL(12,4) comment '开盘标志'
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;


create table FI_QUOTE_HOURLY_HKEX_
(
`DATE` String comment '日期',
`TIME` String comment '日期',
`OPEN` DECIMAL(12,4) comment '开盘价',
HIGH DECIMAL(12,4) comment '最高价',
LOW DECIMAL(12,4) comment '最低价',
CLOSE DECIMAL(12,4) comment '收盘价',
VOLUME DECIMAL(12,4) comment '成交量',
OPEN_INT DECIMAL(12,4) comment '开盘标志'
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

create table FI_QUOTE_5MIN_HKEX_
(
`DATE` String comment '日期',
`TIME` String comment '日期',
`OPEN` DECIMAL(12,4) comment '开盘价',
HIGH DECIMAL(12,4) comment '最高价',
LOW DECIMAL(12,4) comment '最低价',
CLOSE DECIMAL(12,4) comment '收盘价',
VOLUME DECIMAL(12,4) comment '成交量',
OPEN_INT DECIMAL(12,4) comment '开盘标志'
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;