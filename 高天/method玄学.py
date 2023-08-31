#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/8/31 21:15
@file: method玄学
@desc: 
"""


class C:
    def f(self):
        pass


o = C()
a = id(o.f)
# print(a)
b = id(o.f)
print(a)
print(b)
