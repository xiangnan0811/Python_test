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


def init_logger(level="INFO"):
    logger.remove()
    logger.add(sys.stdout, level=level)
    logger.add(
        "./feader.log",
        level="INFO",
        rotation="00:00",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True,
        encoding="utf-8",
    )
    logger.add(
        "./feader_error.log",
        level="WARNING",
        rotation="00:00",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True,
        encoding="utf-8",
    )


if __name__ == "__main__":
    init_logger()
    logger.info("hello world")
    logger.info(logger)
