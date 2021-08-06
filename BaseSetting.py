# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： BasePath.py
# Author : YuYanQing
# Desc: 声明目录结构
# Date： 2020/7/15 16:15
'''
import os

class Route():
    def __init__(self):
        """
        统一配置yaml文件及报告产生的路径
        """
        self.workspaces = os.path.abspath(os.path.dirname(__file__))
        self.path = {"debug":r"debug",
                     "result": r"result",
                     "test_path":r"test_case",
                     "test_data": r"test_data",
                     "global_variables":r"conf/global_variables",
                     "host_properties" :r"conf/host_properties",
                     "user_variables" :r"conf/user_variables",
                     "workspaces": self.workspaces,
                     "allure_result":r"allure_result",
                     "allure_report": r"allure_report",
                     }

    def getPath(self,keyword):
        """
        获取路径
        :param keyword:
        :return:
        """
        if keyword == "workspaces":
            return self.workspaces
        else:
            return os.path.join(self.workspaces,self.path[keyword])

    def joinPath(self,file_path,file_name):
        """
        拼接路径
        :param file_path 文件路径
        :param file_name 文件名
        :return:
        """
        return os.path.join(Route.getPath(file_path), file_name)

Route = Route()

if __name__ == '__main__':
    print(Route.getPath("workspaces"))
    print(Route.getPath("debug"))
    print(Route.joinPath("debug","test_change_type.json"))