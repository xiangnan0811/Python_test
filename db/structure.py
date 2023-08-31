#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/9/4 19:25
@file: structure
@desc: 
"""


class DatabaseConfig:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        # 数据库名有时需要指定
        self.database = database
