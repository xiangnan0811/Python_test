#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: weibo
@contact: weibo@yadingdata.com
@time: 2022/2/6 20:28
@file: running.py
@desc: 运行时配置
"""

# 日志级别
LOG_LEVEL = 'DEBUG'
# LOG_LEVEL = 'INFO'

# 生成任务协程数
ASSEMBLE_COROUTINE = 1
# 下载数据协程数
DOWNLOAD_COROUTINE = 20
# 保存数据协程数
UPLOAD_COROUTINE = 30

# 下载任务时间切分间隔，单位：天
TIME_DELTA = 3

# 单条下载结果对象最大结果数
MAX_RESULT_SIZE = 1000

# 下载任务时间切分间隔，单位：分钟
TIME_INTERVAL = 15

# length of task queue
TASK_QUEUE_LENGTH = 10

# length of result queue
RESULT_QUEUE_LENGTH = 100
