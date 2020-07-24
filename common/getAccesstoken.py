#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time   : 2020/7/24 15:18
# @Author : Eastonliu
# @Desc   :

import requests
import base64


def get_accesstoken(url, username, password):
    """
    根据用户名和密码获取accesstoken
    :param url:
    :param username: 用户名
    :param password: 密码
    :return:
    """
    rec1 = requests.get(r'%s/zuul/api/checkIsFirst' % url, allow_redirects=False)
    redirect_url1 = rec1.headers.get('Location')
    # 获取第二个重定向地址,http://172.21.23.82/cas/?service=http%3A%2F%2F172.21.23.82%2Fzuul%2Fapi%2FcheckIsFirst
    rec2 = requests.get(redirect_url1, allow_redirects=False)
    redirect_url2 = rec2.headers.get('Location')
    # 获取第三个重定向地址 http://172.21.23.82/cas/login?service=http%3A%2F%2F172.21.23.82%2Fzuul%2Fapi%2FcheckIsFirst
    rec3 = requests.get(redirect_url2, allow_redirects=False)
    redirect_url3 = rec3.headers.get('Location')
    # 获取SESSION1
    rec4 = requests.get(redirect_url3, allow_redirects=False)
    SESSION = rec4.cookies.get('SESSION')
    # 获取第四个重定向地址 http://172.21.23.82/zuul/api/checkIsFirst?ticket=ST-46-4Vw3O9p5g6aEIDSNfmecfje05nocms
    _headers = {
        'Cookie': 'SESSION=%s' % SESSION,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'username': username,
        'password': str(base64.b64encode(password.encode()), 'ascii'),
        'execution': 'e1s1',
        '_eventId': 'submit',
        'geolocation': ''
    }
    rec5 = requests.post(redirect_url3, allow_redirects=False, headers=_headers, data=payload)
    redirect_url4 = rec5.headers.get('Location')
    # 获取第五个重定向地址 http://172.21.23.82/zuul/api/checkIsFirst;jsessionid=EBBE8F4E39FBD55A564C4097ED53683D
    rec6 = requests.get(redirect_url4, allow_redirects=False)
    JSESSIONID = rec6.cookies.get('JSESSIONID')
    redirect_url5 = rec6.headers.get('Location')
    # 获取accessToken
    _headers = {
        'Cookie': 'JSESSIONID=%s' % JSESSIONID,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    rec7 = requests.get(redirect_url5, headers=_headers)
    accessToken = rec7.cookies.get('accessToken')
    return accessToken
