#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/23 11:31
# @Author : Eastonliu
# @Desc   :

import pymysql
from common.log import logger


class OperatorMysql(object):
    def __init__(self, config):
        self.config = config
        try:
            self.db = pymysql.connect(**self.config)
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        except ConnectionError as e:
            logger.error(str(e))

    def executesql(self, sql):
        self.cursor.execute(sql)
        self.db.commit()
        return self.cursor

    def getvalue(self, cursor):
        value = cursor.fetchall()
        return value

    def closedb(self):
        self.cursor.close()
        self.db.close()
