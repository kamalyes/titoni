# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Variables.py
# Author : YuYanQing
# Desc: 全局变量池
# Date： 2021/8/11 10:56
'''
from iutils.Loader import Loader
from iutils.YamlUtils import YamlHandle
from testings.control.path import GLOBAL_VAR_PATH

class Global():

    @classmethod
    def setValue(self,obj):
        """
        设置全局变量
        :param obj:
        :return:
        """
        try:
            YamlHandle.saveData(GLOBAL_VAR_PATH,obj,False)
        except KeyError:
            return False

    @classmethod
    def getValue(self,key):
        """
        获取全局变量
        :param key:
        :return:
        """
        try:
            return Loader.yamlFile(GLOBAL_VAR_PATH).get(key)
        except KeyError:
            return False

