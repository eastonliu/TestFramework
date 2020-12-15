#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/12/14 10:00
# @Author : Eastonliu
# @Desc   :

import pytest
from selenium import webdriver
from typing import List
from ui.page.loginPage import LoginPage
from common import URL, GOOGLE_DRIVER, USERNAME, PASSWORD


# 登录
@pytest.fixture()
def login(username=USERNAME, password=PASSWORD):
    driver = webdriver.Chrome(executable_path=GOOGLE_DRIVER)
    page = LoginPage(driver)
    page.get(URL)
    page.maximize_window()
    page.login(username=username, password=password)
    yield page
    driver.close()


# 解决parametrize参数化ids中文控制台显示unicode
def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
