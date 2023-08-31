#!/usr/bin/env python
"""
@author: weibo
@contact: weibo@yadingdata.com
@time: 2022/1/27 16:07
@file: structure.py
@desc: oracle 配置类
"""
from db.structure import DatabaseConfig


class OracleConfig(DatabaseConfig):
    def __init__(self, host, port, service_name, user, password, database):
        super().__init__(host, port, user, password, database)
        self.service_name = service_name
