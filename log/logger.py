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
import logging

from loguru import logger

from config.env import log_path
from config.running import LOG_LEVEL


# 将 loguru 的 logger 用作一个日志处理器
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # 获取对应的 loguru 方法
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def init_logger(other_modulle: str|None = None, log_file_name: str|None = None, remove_existing_handlers: bool = True):
    """
    初始化日志模块
    :return:
    """
    # 日志格式
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | " \
                "<cyan>Process-{process}</cyan>:<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    # 日志文件
    if not log_file_name:
        log_file_name = "log"
    if other_modulle:
        # 将 InterceptHandler 添加到 other_modulle 的日志处理器中
        logging.getLogger(other_modulle).handlers = [InterceptHandler()]
        logging.getLogger(other_modulle).setLevel(LOG_LEVEL)
    if remove_existing_handlers:
        for handler in logger._core.handlers: # pylint: disable=protected-access # type: ignore
            logger.remove(handler)
    logger.add(sys.stderr, level=LOG_LEVEL, format=log_format)
    logger.add(
        f"{log_path}/{log_file_name}.log",
        level=LOG_LEVEL,
        format=log_format,
        rotation="1 day",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )

    return logger
