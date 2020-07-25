#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/25 10:56
# @Author : Eastonliu
# @Desc   :

from ui.baseobject.page import Page
from ui.baseobject.pageobject import PageElement


class HomePage(Page):
    home_text = PageElement(class_name='shortcut', describe='右上角首页文字')
