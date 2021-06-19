# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： test_registerv2_succeed.py
# Author : YuYanQing
# Desc: 注册成功
# Date： 2021/6/15 20:55
'''
import pytest

class TestRegisterV2_Succeed():
    @pytest.mark.run(order=1)
    def test_001(self):
        assert 1==2
        print("注册失败")

    @pytest.mark.run(order=2)
    @pytest.mark.smoke
    def test_002(self):
        assert 1==1
        print("注册成功")

    @pytest.mark.run(order=3)
    def test_003(self):
        assert 1==2
        print("注册失败")