# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： data.py
# Author : YuYanQing
# Desc:  变量池
# Date： 2021/8/19 9:46
'''
from iutils.Loader import Loader
from testings.control.path import APPLICATION_PATH

APPLICATION = Loader.yamlFile(APPLICATION_PATH)
DB_CONFIG = APPLICATION["database"]