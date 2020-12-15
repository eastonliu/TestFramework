#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/25 11:05
# @Author : Eastonliu
# @Desc   :

import pytest
import unittest
from selenium import webdriver
import math
import random
from common import URL, GOOGLE_DRIVER, USERNAME, PASSWORD
from ui.page.loginPage import LoginPage
from ui.page.comPage import ComPage


class TestLogin:
    """
    登录功能
    """
    data1 = [
        (USERNAME, PASSWORD, "首页")
    ]

    @pytest.mark.parametrize("username,password,expect", data1, ids=[
        "账号密码正确，登录成功",
    ])
    def test_00(self, login, username, password, expect):
        """
        用户名和密码正确，登陆成功
        :return:
        """
        home_text = ComPage(login.driver).home_text.text
        assert home_text == expect

    data2 = [
        ("POLHKITR", PASSWORD, "用户信息不存在"),
        (USERNAME, math.floor(1e8 * random.random()), "用户名或密码错误"),
    ]

    @pytest.mark.parametrize("username,password,expect", data2, ids=[
        "账号不存在，登录失败",
        "账号正确，密码错误，登录失败"
    ])
    def test_01(self, login, username, password, expect):
        """
        用户名和密码不匹配，登录失败
        :return:
        """
        result_text = login.msg_login.text
        assert result_text == expect

