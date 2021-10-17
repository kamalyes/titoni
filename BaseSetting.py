# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： BasePath.py
# Author : YuYanQing
# Desc: 声明目录结构
# Date： 2020/7/15 16:15
"""
import os


class Route(object):
    def __init__(self):
        """
        统一配置yaml文件及报告产生的路径
        """
        self.workspaces = os.path.abspath(os.path.dirname(__file__))
        self.path = {"output": "output",
                     "config": "config",
                     "debug": "debug",
                     "report_data": "summary.yaml",
                     "allure_result": "allure_result",
                     "allure_report": "allure_report",
                     "test_path": r"testings",
                     "service": r"testings/service",
                     "test_img": r"testings/dao/test_img",
                     "test_csv": r"testings/dao/test_csv",
                     "test_json": r"testings/dao/test_json",
                     "test_yaml": r"testings/dao/test_yaml",
                     "auto_exec": r"testings/service/auto_exec",
                     "properties": r"testings/config/properties",
                     "variables": r"testings/config/variables",
                     "localhost": r"testings/config/localhost",
                     }

    def getPath(self, keyword, security=None):
        """
        获取路径
        :param keyword:
        :param security: 是否安全加载
        :return:
        """
        try:
            if keyword == "workspaces":
                return self.workspaces
            else:
                if security:
                    try:
                        return os.path.join(self.workspaces, self.path[keyword])
                    except KeyError:
                        return keyword
                else:
                    return os.path.join(self.workspaces, self.path[keyword])
        except KeyError:
            raise KeyError("全局路径中未配置%s" % (keyword))

    def joinPath(self, file_path, file_name):
        """
        拼接路径
        :param file_path 文件路径
        :param file_name 文件名
        :return:
        """
        return os.path.join(Route.getPath(file_path), file_name)


Route = Route()
