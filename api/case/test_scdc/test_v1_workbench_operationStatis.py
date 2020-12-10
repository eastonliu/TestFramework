#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/12/8 10:07
# @Author : Eastonliu
# @Desc   :

import pytest
import os
import requests
from common import URL, API_PATH
from common.readYaml import YamlReader

uc_yaml_path = os.path.join(API_PATH, 'data', 'scdc', 'scdc.yaml')


class TestSysMenus:
    """
    获取运营统计V1接口/api/v1/workbench/operationStatis
    """

    def setup_class(self):
        self.yaml = YamlReader(uc_yaml_path)
        self.index = self.yaml.get_index('/api/v1/workbench/operationStatis')
        self.url = URL + '/zuul/scdc' + self.yaml.get('url', self.index)

    def test_00(self,accesstoken):
        """
        获取运营统计数据成功
        :return:
        """
        data = self.yaml.get('body', self.index)
        rec = requests.post(url=self.url, json=data, headers={'accessToken': accesstoken})
        code = rec.json()["returnCode"]
        assert code == "200"


if __name__ == '__main__':
    pytest.main(["-v"])
