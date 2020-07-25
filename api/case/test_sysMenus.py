#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/9 11:47
# @Author : Eastonliu
# @Desc   :


import unittest
import os
import requests
from common import URL, HEADERS, API_PATH
from common.readYaml import YamlReader

uc_yaml_path = os.path.join(API_PATH, 'data', 'uc', 'uc.yaml')


class TestSysMenus(unittest.TestCase):
    """
    获取应用菜单树V2接口/api/v1/portal/sysMenus
    """

    @classmethod
    def setUpClass(cls):
        cls.yaml = YamlReader(uc_yaml_path)
        cls.index = cls.yaml.get_index('/api/v1/portal/sysMenus')
        cls.url = URL + '/zuul/uc' + cls.yaml.get('url', cls.index)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_00(self):
        """获取菜单成功"""
        data = self.yaml.get('body', self.index)
        rec = requests.post(url=self.url, json=data, headers=HEADERS)
        code = rec.json()["returnCode"]
        self.assertEqual(code, "200")

    def test_01(self):
        """sysCode为空"""
        data = self.yaml.get('body', self.index)
        data['sysCode'] = ""
        rec = requests.post(url=self.url, json=data, headers=HEADERS)
        code = rec.json()["returnCode"]
        self.assertEqual(code, "200")


if __name__ == '__main__':
    unittest.main()
