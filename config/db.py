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
    host='',
    port='',
    service_name='',
    user='',
    password='',
    database=''
)

mysql_config = MySQLConfig(
    host='',
    port=0,
    user='',
    password='',
    database='tk',
)

local_mysql_config = MySQLConfig(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='lxs',
)
