#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/6/28 17:54
# @Author : Eastonliu
# @Desc   :

from selenium.webdriver.common.by import By
from common.exceptions import FindElementTypesError

LOCATOR_LIST = {
    'id_': By.ID,
    'name': By.NAME,
    'class_name': By.CLASS_NAME,
    'tag': By.TAG_NAME,
    'link_text': By.LINK_TEXT,
    'partial_link_text': By.PARTIAL_LINK_TEXT,
    'xpath': By.XPATH,
    'css': By.CSS_SELECTOR
}


class PageObject(object):
    def __init__(self):
        pass


class PageElement(object):
    def __init__(self, timeout=5, describe="undefined", index=0, **kwargs):
        self.timeout = timeout
        self.index = index
        self.desc = describe
        if not kwargs:
            raise ValueError("没有指定定位元素！")
        if len(kwargs) > 1:
            raise ValueError("指定了多个定位元素！")
        self.kwargs = kwargs
        self.k, self.v = kwargs.items()
        if self.k not in LOCATOR_LIST:
            raise FindElementTypesError("不支持这种%s定位方法！"%self.k)
        
