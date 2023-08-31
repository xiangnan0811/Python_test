#!/usr/bin/env python
"""
@author: weibo
@contact: weibo@yadingdata.com
@time: 2022/1/27 17:15
@file: connection.py
@desc: oracle 连接池
"""
import cx_Oracle_async
from cx_Oracle_async.pools import AsyncPoolWrapper

from common import SingletonType
from .struct import OracleConfig


class ConnectionPool(metaclass=SingletonType):
    __pool = None

    def __init__(self, oracle_config: OracleConfig):
        self.oracle_config = oracle_config

    # 创建数据库连接池
    async def get_pool(self) -> AsyncPoolWrapper:
        if not self.__pool:
            self.__pool: AsyncPoolWrapper = await cx_Oracle_async.create_pool(
                host=self.oracle_config.host,
                port=self.oracle_config.port,
                user=self.oracle_config.user,
                password=self.oracle_config.password,
                service_name=self.oracle_config.service_name,
                min=1,
                max=20,
                waitTimeout=180,
            )
        return self.__pool
