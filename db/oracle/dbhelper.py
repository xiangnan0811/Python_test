#!/usr/bin/env python
"""
@author: weibo
@contact: weibo@yadingdata.com
@time: 2022/1/27 17:15
@file: dbhelper.py
@desc: oracle 封装
"""
import cx_Oracle

from .connection import ConnectionPool
from cx_Oracle_async.cursors import AsyncCursorWrapper
from cx_Oracle_async.pools import AsyncPoolWrapper


class DBHelper(object):

    def __init__(self):
        ...

    @staticmethod
    def rows_to_dict_list(cursor: AsyncCursorWrapper, result):
        columns = [i[0] for i in cursor._cursor.description]
        return [dict(zip(columns, row)) for row in result]

    @staticmethod
    def output_type_handler(cursor, name, default_type, size, precision, scale):
        if default_type == cx_Oracle.DB_TYPE_NCLOB:
            return cursor.var(cx_Oracle.LONG_STRING, arraysize=cursor.arraysize)
        if default_type == cx_Oracle.DB_TYPE_CLOB:
            return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)
        if default_type == cx_Oracle.DB_TYPE_BLOB:
            return cursor.var(cx_Oracle.DB_TYPE_LONG_RAW, arraysize=cursor.arraysize)

    # @staticmethod
    # async def select_result(sql, config, param=None) -> list:
    #     """
    #     查询数据
    #     :param sql:
    #     :param param:
    #     :param config:
    #     :return:
    #     """
    #     db = ConnectionPool(config)
    #     async with db:
    #         if param is None:
    #             await db.cursor.execute(sql)
    #         else:
    #             await db.cursor.execute(sql, param)
    #         # 原始调用返回元组
    #         result = await db.cursor.fetchall()
    #         # 返回dict
    #         result = DBHelper.rows_to_dict_list(db.cursor, result)
    #     return result

    @staticmethod
    async def select_result(sql, config, param=None, result_type='dict') -> list:
        """
        查询数据
        :param sql:
        :param param:
        :param config:
        :param result_type:
        :return:
        """
        db = ConnectionPool(config)
        pool: AsyncPoolWrapper = await db.get_pool()
        async with pool.acquire() as conn:
            conn._conn.outputtypehandler = DBHelper.output_type_handler
            async with conn.cursor() as cursor:
                if param is None:
                    await cursor.execute(sql)
                else:
                    await cursor.execute(sql, param)
                # 原始调用返回元组
                result = await cursor.fetchall()
                # 返回dict
                if result_type == 'dict':
                    result = DBHelper.rows_to_dict_list(cursor, result)
        return result
