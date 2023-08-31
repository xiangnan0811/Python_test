#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: weibo
@contact: weibo@yadingdata.com
@time: 2022/5/7 15:13
@file: dbhelper
@desc: 
"""
import  motor.motor_asyncio
from motor.core import AgnosticCollection, AgnosticDatabase

from log import Logger
from config.running import LOG_LEVEL


class DBHelper:

    def __init__(self, mongo_url, mongo_db):
        self.mc = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        self.db: AgnosticDatabase = self.mc[mongo_db]
        self.logger = Logger(LOG_LEVEL)

    @staticmethod
    async def create_index(index_keys: list, coll: AgnosticCollection):
        """
        create index
        :param index_keys:  index keys
        :param coll:        collection
        :return:            None
        """
        _keys = [(key, 1) for key in index_keys]
        await coll.create_index(_keys, unique=False)

    def get_collection(self, coll, **kwargs) -> AgnosticCollection:
        """
        get collection
        :param coll:    collection name
        :return:        AgnosticCollection
        """
        return self.db.get_collection(coll, **kwargs)

    async def insert_many(self, data: list, coll_name: str, index_keys: list=None):
        """
        insert many data
        :param data:           data list
        :param coll_name:      collection name
        :param index_keys:     index keys
        :return:               insert count
        """
        # 1. get collection
        coll: AgnosticCollection = self.get_collection(coll_name)
        # 2. create indexes
        if index_keys is not None:
            await self.create_index(index_keys, coll)
        # 3. insert many
        insert_res = await coll.insert_many(data)
        # 4. return insert count
        if insert_res.acknowledged:
            return len(insert_res.inserted_ids)
        return 0

    async def find_one(self, coll_name: str, _filter: dict=None, projection: dict=None):
        """
        find one data
        :param coll_name:      collection name
        :param _filter:         filter
        :param projection:     projection
        :return:               data
        """
        # 1. get collection
        coll: AgnosticCollection = self.get_collection(coll_name)
        # 2. find one
        if _filter is None:
            _filter = {}
        data = await coll.find_one(_filter, projection)
        # 3. return data
        return data
