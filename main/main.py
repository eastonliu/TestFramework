#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/30 11:12
# @Author : Eastonliu
# @Desc   :


import unittest
from common import REPORT_PATH, API_CASE_PATH, UI_CASE_PATH
from common.HTMLTestRunner import HTMLTestRunner

all_case = unittest.defaultTestLoader.discover(start_dir=UI_CASE_PATH,pattern='test*.py',top_level_dir=None)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(all_case)

