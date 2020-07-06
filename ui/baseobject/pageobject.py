#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/6/28 17:54
# @Author : Eastonliu
# @Desc   :

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from common.exceptions import FindElementTypesError
from common import log

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
    def __init__(self, driver, url=None):
        self.driver = driver
        self.root_uri = url if url else getattr(self.driver, 'url', None)

    def get(self, uri):
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)


class PageElement(object):
    def __init__(self, context=False, describe="undefined", **kwargs):
        self.desc = describe
        if not kwargs:
            raise ValueError("Please specify a locator")
        if len(kwargs) > 1:
            raise ValueError("Please specify only one locator")
        self.k, self.v = next(iter(kwargs.items()))
        try:
            self.locator = (LOCATOR_LIST[self.k], self.v)
        except KeyError:
            raise FindElementTypesError("Element positioning of type '{}' is not supported. ".format(self.k))
        self.has_context = context

    def find(self, context):
        try:
            return context.find_element(*self.locator)
        except NoSuchElementException:
            return None

    def __get__(self, instance, owner, context=None):
        if not instance:
            return None
        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)
        if not context:
            context = instance.driver
        return self.find(context)

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("Can't set value, element not found")
        elem.send_keys(value)


class PageElements(PageElement):

    def find(self, context):
        try:
            return context.find_elements(*self.locator)
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise ValueError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]
