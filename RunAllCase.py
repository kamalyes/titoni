# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RunAllCase.py
# Author : YuYanQing
# Desc: PyCharm
# Date： 2021/3/27 17:28
'''
import pytest

if __name__ == '__main__':
    pytest.main(["-vs","-m" "smoke",r"D:\Work_Spaces\PyCharm_Project\YamlInterfaceTest\TestCase\test_registerv2_succeed.py"])