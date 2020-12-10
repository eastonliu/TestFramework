#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/12/10 10:34
# @Author : Eastonliu
# @Desc   :

import pytest
from common import URL, USERNAME, PASSWORD


@pytest.fixture(name="accesstoken")
def get_accesstoken(url=URL, username=USERNAME, password=PASSWORD):
    from common.getAccesstoken import get_accesstoken
    return get_accesstoken(url=url, username=username, password=password)
