#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/8 9:39
# @Author : Eastonliu
# @Desc   : 对Yaml文件的操作

import yaml
import os


class YamlReader(object):
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError("文件不存在！")
        self._data = None

    @property
    def data(self):
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = yaml.load(f, Loader=yaml.FullLoader)
        return self._data

    def get(self, element, index=0):
        return self.data[index].get(element)

    def get_index(self, url):
        """
        根据url获取接口的index
        :param url:
        :return:
        """
        urls = []
        for elem in self.data:
            urls.append(elem.get('url'))
        return urls.index(url)
