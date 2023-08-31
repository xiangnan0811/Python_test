#!/usr/bin/env python
"""
@author: weibo
@contact: weibo@yadingdata.com
@time: 2022/5/1 16:04
@file: db.py
@desc: 各项数据库配置
"""
from db.oracle import OracleConfig
from db.aiomysql import MySQLConfig

oracle_config = OracleConfig(
    host='47.108.151.116',
    port='12458',
    service_name='lxs_item',
    user='lxs_item',
    password='lxs67890prod',
    database='lxs_item'
)

mysql_config = MySQLConfig(
    host='47.108.151.116',
    port=17649,
    user='toor',
    password='nyn^B2!g^V@57omO^JYr',
    database='tk',
)

local_mysql_config = MySQLConfig(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='lxs',
)
