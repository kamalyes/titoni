# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Variables.py
# Author : YuYanQing
# Desc: 全局变量
# Date： 2021/7/30 8:53
'''
from BaseSetting import Route
from iutils.Loader import Loader
from iutils.YamlUtils import YamlHandle

class Global():
    def __init__(self):
        """
        初始化
        """
        self.path = Route.joinPath("user_variables", "global.yaml")

    def initValue(self):
        return Loader.yamlFile(self.path)

    def setValue(self,obj):
        """
        设置全局变量
        :param obj:
        :return:
        """
        try:
            YamlHandle.saveData(self.path,obj,False)
        except KeyError:
            return False

    def getValue(self,key):
        """
        设置全局变量
        :param key:
        :return:
        """
        try:
            return self.initValue()[key]
        except KeyError:
            return False

if __name__ == '__main__':
    gl = Global()
    init_data = gl.initValue()
    gl.setValue({"catyid":199997})
    fix_data = gl.initValue()
    print("修改前的值：",init_data,"修改后的值：",fix_data)
    get_data = gl.getValue("category_id")
    print(type(get_data),get_data)