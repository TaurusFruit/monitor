# DESCRIPTION

zabbix 微信程序
zabbix 通过微信企业账号报警，可点进报警页面查看详细情况

通过zabbix 数据库获取相关内容
通过zabbix API执行相关操作


1. 报警功能
    1. 通过微信企业账号报警,按照用户组报警
    2. 报警信息可点进入报警详细页面
    3. 报警详细页面可查看包括:
        1. 当前报警内容
        2. 提交知悉内容
        3. 查看历史报警记录
        4. 查看当前主机触发器状态
        5. 查看主机CPU/内存/流量图

2. 快捷操作
    1. 快捷增加报警模板
    2. 快捷删除/停止报警配置



------------
2017.1.9  更新内容

- 增加用户信息表 contect.py 定义用户组等信息

- 增加获取微信命令功能
    - 按组获取top流量
    - 按组获取top负载

