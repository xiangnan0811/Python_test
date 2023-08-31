#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: weibo
@contact: weibo@yadingdata.com
@time: 2022/1/27 17:59
@file: env.py
@desc: 
"""

from pathlib import Path

# 日志文件夹,默认为同级目录的_log文件夹下
log_path = "./_log"
Path(log_path).mkdir(exist_ok=True, parents=True)

# 时间格式
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
# 日期格式
DATE_FORMAT = "%Y-%m-%d"
