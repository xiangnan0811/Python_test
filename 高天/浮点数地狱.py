#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/8/31 20:37
@file: 浮点数地狱
@desc: 
"""
from objprint import op

op.config(arg_name=True)

op(0.1 + 0.2 == 0.3)
op(1e50 == 10 ** 50)

op(1e500 == 1e600)
op(1e500 > 10 ** 1000)
op(1e500 * 1e500 > 0)
op(1e500 / 1e500 > 0)
op(1e500 / 1e500 == 1e500 / 1e500)
