
# Sql: 关于时间与日期

##### 本月

`DATE_FORMAT(t_orders.createTime,'%Y-%m')=DATE_FORMAT((now()),'%Y-%m')`

##### 上月

`DATE_FORMAT(t_orders.createTime,'%Y-%m')=DATE_FORMAT(date_sub(now(), INTERVAL 1 MONTH),'%Y-%m')`

##### 本周

`YEARWEEK(DATE_FORMAT(t_orders.createTime, '%Y-%m-%d')) = YEARWEEK(now())`