#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/6 17:11
# @Author : Eastonliu
# @Desc   :

from ui.baseobject.pageobject import PageObject


class Page(PageObject):
    def execute_script(self, js=None, *args):
        """
        Execute JavaScript scripts.
        """
        if js is None:
            raise ValueError("Please input js script")

        return self.driver.execute_script(js, *args)

    def maximize_window(self):
        self.driver.maximize_window()
