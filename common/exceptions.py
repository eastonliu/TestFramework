#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/6/29 9:46
# @Author : Eastonliu
# @Desc   :


class Exceptions(Exception):
    def __init__(self, msg=None, screen=None, stacktrace=None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = "Message:%s\n" % self.msg
        return exception_msg


class FindElementTypesError(Exceptions):
    pass
