#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Description: 
@Date       : 2022/05/04 22:31:25
@Author     : weibo
"""
import aiomysql

from .struct import MySQLConfig
from common import SingletonType


class ConnectionPool(metaclass=SingletonType):
    __pool = None

    @classmethod
    async def get_pool(cls, config):
        if not cls.__pool:
            cls.__pool = await aiomysql.create_pool(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                db=config.database,
                charset=config.charset,
                maxsize=config.maxsize,
                minsize=config.minsize,
            )
        return cls.__pool
