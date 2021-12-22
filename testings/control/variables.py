# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： Variables.py
# Author : YuYanQing
# Desc: 全局变量池
# Date： 2021/8/11 10:56
"""
import os
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
        YamlHandle.saveData(GLOBAL_VAR_PATH,obj,False)

    @classmethod
    def getValue(self,key=None):
        """
        获取全局变量
        :param key:
        :return:
        """
        try:
            value = Loader.yamlFile(GLOBAL_VAR_PATH)
            if key is None:
                return value
            else:
                return value.get(key)
        except KeyError:
            return False

