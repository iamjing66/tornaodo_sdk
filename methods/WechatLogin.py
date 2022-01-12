#!/usr/bin/env python
# coding=utf-8

import requests
from urllib.parse import quote
import hashlib
import time
import xmltodict

class WechatLogin(object):

    def __init__(self):

        self.Appid = "wx74b1fd3e0df1b73a"
        self.AppSecret = "3394704c3f91a9eadc1f8e1863bf7bfd"
        self.CodeUrl = "https://open.weixin.qq.com/connect/qrconnect?appid=%s&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect"
        self.REDIRECT_URI = 'http://your_domain.com/redirect_uri'
