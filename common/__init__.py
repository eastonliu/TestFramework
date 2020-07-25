#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/6 17:19
# @Author : Eastonliu
# @Desc   :

import os
from common.readYaml import YamlReader
from common.getAccesstoken import get_accesstoken

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yaml')
STATIC_PATH = os.path.join(BASE_PATH, 'static')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
GOOGLE_DRIVER = os.path.join(BASE_PATH, 'drivers','chromedriver.exe')
API_PATH = os.path.join(BASE_PATH, 'api')
LOGS_PATH = os.path.join(BASE_PATH, 'logs')
USERNAME = YamlReader(CONFIG_FILE).data['username']
PASSWORD = YamlReader(CONFIG_FILE).data['password']
URL = YamlReader(CONFIG_FILE).data['host']
ACCESSTOKEN = get_accesstoken(url=URL, username=USERNAME, password=PASSWORD)
HEADERS = {
    'accessToken': ACCESSTOKEN
}
