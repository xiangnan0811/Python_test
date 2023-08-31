#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/8/31 17:39
@file: 三个看似一样的列表
@desc: 
"""
import sys
import dis

a = [0] * 3
b = [0, 0, 0]
c = [0 for _ in range(3)]
print(sys.getsizeof(a))
print(sys.getsizeof(b))
print(sys.getsizeof(c))

print(dis.dis('[0] * 3'), f'\n{"-" * 100}\n')
print(dis.dis('[0, 0, 0]'), f'\n{"-" * 100}\n')
print(dis.dis('[0 for _ in range(3)]'), f'\n{"-" * 100}\n')
