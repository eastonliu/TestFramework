#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/25 11:05
# @Author : Eastonliu
# @Desc   :


import unittest
from selenium import webdriver
import math
import random
from common import URL, GOOGLE_DRIVER, USERNAME, PASSWORD
from ui.baseobject.page import Page
from ui.page.loginPage import LoginPage
from ui.page.homePage import HomePage


class TestLogin(unittest.TestCase):
    """
    登录功能
    """

    def setUp(self) -> None:
        self.driver = webdriver.Chrome(executable_path=GOOGLE_DRIVER)
        self.page = LoginPage(self.driver)
        self.page.get(URL)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()

    def test_00(self):
        """
        用户名和密码正确，登陆成功
        :return:
        """
        self.page.login(username=USERNAME, password=PASSWORD)
        HomePage(self.driver)
        home_text = HomePage(self.driver).home_text.text
        self.assertEqual(home_text, "首页")

    def test_01(self):
        """
        用户名和密码不匹配，登录失败
        :return:
        """
        # 随机生成一个8位数的密码
        pwd = math.floor(1e8 * random.random())
        self.page.login(username=USERNAME, password=pwd)
        result_text = self.page.msg_login.text
        self.assertEqual(result_text, "用户名或密码错误")


if __name__ == '__main__':
    unittest.main(verbosity=2)
