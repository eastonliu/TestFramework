#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/6/29 11:40
# @Author : Eastonliu
# @Desc   : 日志模块封装

import os
import time
import logging.handlers
from logging.handlers import TimedRotatingFileHandler

root_dir = os.path.dirname(os.path.dirname(__file__))
logs_dir = os.path.join(root_dir, 'logs')
log_names = ['debug', 'error', 'info']
for name in log_names:
    if not os.path.exists(os.path.join(logs_dir, name)):
        os.makedirs(os.path.join(logs_dir, name))
dir_time = time.strftime('%Y-%m-%d', time.localtime())
pattern = '%(asctime)s-%(levelname)s:%(message)s'
handlers = {
    logging.DEBUG: os.path.join(logs_dir, 'debug/debug_%s.log' % dir_time),
    logging.INFO: os.path.join(logs_dir, 'info/info_%s.log' % dir_time),
    logging.ERROR: os.path.join(logs_dir, 'error/error_%s.log' % dir_time)
}

logger = logging.getLogger()
logging.root.setLevel(logging.NOTSET)
handler_console = logging.StreamHandler()
handler_console.setFormatter(logging.Formatter(pattern))
handler_console.setLevel(logging.DEBUG)
logger.addHandler(handler_console)

logLevels = handlers.keys()
for level in logLevels:
    path = os.path.abspath(handlers[level])
    handlers[level] = TimedRotatingFileHandler(filename=path,
                                               when='D',
                                               interval=1,
                                               backupCount=5,
                                               delay=True,
                                               encoding='utf-8'
                                               )
    handlers[level].setLevel(level)
    handlers[level].setFormatter(logging.Formatter(pattern))
    logger.addHandler(handlers[level])


def debug(msg):
    logger.debug(str(msg))


def info(msg):
    logger.info(str(msg))


def error(msg):
    logger.error(str(msg))



