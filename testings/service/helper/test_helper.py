# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_helper.py
# Author : YuYanQing
# Desc: 测试函数助手
# Date： 2021/8/31 10:25
'''
from iutils.OkHttps import Httpx
from testings.control.init import Envision

config = Envision.getYaml("test_helper.yaml")['config']
test_setup = Envision.getYaml("test_helper.yaml")['test_setup']

class TestHelper():
    def test_helper_test_get(self):
        Httpx.sendApi(auto=True, esdata=[config,test_setup["search_001"]])

    def test_helper_test_post(self):
        Httpx.sendApi(auto=True, esdata=[config,test_setup["search_002"]])