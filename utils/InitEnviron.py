# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： InitEnviron.py
# Author : YuYanQing
# Desc: 初始化运行环境
# Date： 2021/6/11 15:15
'''
from BaseSetting import AbsPath
from utils.LogHander import Logger

class IniVariable:
    def __init__(self):
        self.logger = Logger().writeLog()
        self.ini_path = "%s\\conf"%(AbsPath)
