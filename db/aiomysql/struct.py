#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/5/4 22:46
@file: struct
@desc: 
"""
from db.structure import DatabaseConfig


class MySQLConfig(DatabaseConfig):
    def __init__(self, host, port, user, password, database):
        super().__init__(host, port, user, password, database)

        self.charset = 'utf8mb4'
        self.maxsize = 100
        self.minsize = 5
