#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: weibo
@contact: weibo@yadingdata.com
@time: 2022/1/27 17:58
@file: logger.py
@desc: 日志模块
"""

import sys

from loguru import logger

from config.env import log_path
from config.running import LOG_LEVEL

Logger = logger
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | " \
             "<cyan>Process-{process}</cyan>:<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
Logger.remove(0)
Logger.add(sys.stderr, level=LOG_LEVEL, format=log_format)
Logger.add(
    f"{log_path}/log.log",
    level=LOG_LEVEL,
    format=log_format,
    rotation="1 day",
    retention="30 days",
    compression="zip",
    backtrace=True,
    diagnose=True,
    enqueue=True,
)
