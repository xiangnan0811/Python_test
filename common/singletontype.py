#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/9/4 15:31
@file: singletontype
@desc: 
"""
import threading
from weakref import WeakValueDictionary


class SingletonType(type):
    # 继承元类
    _instance_lock = threading.Lock()
    _instance = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            with cls._instance_lock:
                if cls not in cls._instance:
                    inst = super(SingletonType, cls).__call__(*args, **kwargs)
                    cls._instance[cls] = inst
        return cls._instance[cls]
