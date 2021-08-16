# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： init.py
# Author : YuYanQing
# Desc: 初始化运行环境
# Date： 2021/8/11 13:25
'''
from BaseSetting import Route
from iutils.Loader import Loader
from testings.control.path import APPPROPERTIES_PATH

class Envision(object):
    def __init__(self):
        self.profiles =Loader.yamlFile(APPPROPERTIES_PATH)["profiles"]

    def getYaml(self,file_name):
        """
        读取Yaml
        :param file_name:
        :return:
        """
        return Loader.yamlFile(Route.joinPath("test_yaml", file_name))

    def getJson(self,file_name):
        """
        读取Json
        :param file_name:
        :return:
        """
        return Loader.jsonFile(Route.joinPath("test_json", file_name))

    def getCsv(self,file_name):
        """
        读取Csv
        :param file_name:
        :return:
        """
        return Loader.csvFile(Route.joinPath("test_csv", file_name))

    def getImg(self,file_name):
        """
        读取Image
        :param file_name:
        :return:
        """
        return Loader.csvFile(Route.joinPath("test_img", file_name))

Envision = Envision()

