#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/6/29 11:40
# @Author : Eastonliu
# @Desc   : 日志模块封装

import os
import time
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
from common import LOGS_PATH

dir_time = time.strftime('%Y-%m-%d', time.localtime())
pattern = '%(asctime)s-%(levelname)s:%(message)s'
logger = logging.getLogger('TestFramework')
logger.setLevel(logging.DEBUG)
handler_console = logging.StreamHandler()
handler_console.setFormatter(logging.Formatter(pattern))
logger.addHandler(handler_console)
handler_file = TimedRotatingFileHandler(filename=os.path.join(LOGS_PATH, 'info_%s.log' % dir_time),
                                        when='D',
                                        interval=1,
                                        backupCount=5,
                                        delay=True,
                                        encoding='utf-8'
                                        )
handler_file.setFormatter(logging.Formatter(pattern))
logger.addHandler(handler_file)
