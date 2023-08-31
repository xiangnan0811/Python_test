#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/9/14 14:19
@file: 自定义类型的对象可以成为字典的键值么
@desc: 
"""


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Position({self.x}, {self.y})"


if __name__ == '__main__':
    d = {}
    p1 = Position(1, 1)
    print(p1)
    p2 = Position(1, 1)
    print(p1 == p2)
    d[p1] = 1
    d[p2] = 2
    print(d)
