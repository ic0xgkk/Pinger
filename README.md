# Pinger

一个没什么用的小工具

## 诞生背景

学校办公网的交换机都打开了端口隔离，以至于ping该地址块内地址无法ping通，自然也无法判断该IP有没有人在使用。印象里好像就算IP冲突操作系统也不会提示了，只能依靠感觉判断是否冲突，即时而丢包时而不丢，这个由ARP的老化时间决定，非常影响网络体验。鉴于此，我在另外一个地址块内执行该程序去持续观测一个地址块内IP的使用情况来判断哪些IP空闲

（顺便再吐槽一下）

## 文件说明

* Init.SQL
 数据库初始化语句，默认已经给了空数据库文件**pinger_blank.db**
* pinger.db
 SQLite3的数据库文件，就这一个小东西没必要用MariaDB的大数据库，SQLite3够用了。用过一次后直接删了再用blank重新覆盖一个就可以继续用了

## 效果

没有效果图，但是亲测就是好用。

今天整了整GayHub，把一些小东西文档补了一下，而已

## 使用方法

1. 看代码第8行，修改**target_cidr**为需要观测的地址块，仅仅支持CIDR表示法
2. 代码第9行，修改**ping_delay**为每个线程ping一次结束后的等待时间，单位为秒
3. 运行一段时间
4. 使用SQL语句分析，此处只给出来一条统计全程未占用的IP的语句
```SQL
SELECT DstIP FROM (SELECT DstIP, SUM(Delay) AS DS FROM `10_0_x_0_24_20190116` GROUP BY DstIP) AS ALT WHERE DS=0;
```
