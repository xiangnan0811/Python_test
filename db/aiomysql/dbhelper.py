#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/5/4 23:11
@file: dbhelper
@desc: 
"""
from aiomysql.cursors import DictCursor, Cursor
from pymysql.err import InternalError

from .connection import ConnectionPool


class DBHelper(object):

    def __init__(self):
        ...

    @staticmethod
    async def select_result(sql, config, result_type='dict', param=None) -> list:
        """查询数据.

        :param sql:
        :param param:
        :param config:
        :param result_type:
        :return:
        """
        if result_type == 'dict':
            cursor_type = DictCursor
        else:
            cursor_type = Cursor
        pool = await ConnectionPool.get_pool(config=config)
        async with pool.acquire() as conn:
            async with conn.cursor(cursor_type) as cursor:
                if param is None:
                    await cursor.execute(sql)
                else:
                    await cursor.execute(sql, param)
                # 原始调用返回元组
                result = await cursor.fetchall()
        return result

    @staticmethod
    async def insert_many(sql, data, config):
        """批量插入数据.

        :param sql:
        :param data:
        :param config:
        :return:
        """
        pool = await ConnectionPool.get_pool(config=config)
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    count = await cursor.executemany(sql, data)
                    await conn.commit()
                except InternalError as e:
                    print(e)
                    count = 0
        return count
