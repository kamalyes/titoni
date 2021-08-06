# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Initialize.py
# Author : YuYanQing
# Desc: 初始化运行环境
# Date： 2021/6/11 15:15
'''
import os
import sys
sys.path.append('../')
from BaseSetting import Route
from inside_utils.LogUtils import Logger
from inside_utils.Loader import Loader

class Env():
    def __init__(self):
        self.logger = Logger.writeLog()
        self.properties =Loader.yamlFile(
            os.path.join(Route.getPath("workspaces"),
            "application.properties.yaml"))["profiles"]
        self.host_dir = "host_properties"
        self.global_dir  = "global_variables"
        self.user_var_dir = "user_variables"

    def getHost(self,host):
        """
        获取自定义的域名
        :param host
        :return:
        """
        try:
            return str(Loader.yamlFile(os.path.join(Route.getPath(self.host_dir),"%s.yaml"%(str(self.properties))))[host])
        except Exception as e:
            self.logger.error("键值：%s未在%s中定义"%(host,self.host_dir))

    def getAwenAdders(self,adders):
        """
        获取后台的地址
        :param adders 地址key
        :return:
        """
        try:
            return str(Loader.yamlFile(os.path.join(Route.getPath(self.global_dir),"manager_path.yaml"))[adders])
        except Exception as e:
            self.logger.error("键值：%s未在%s中定义"%(adders,self.global_dir))

    def getBlockeAdders(self,adders):
        """
        获取小程序的地址
        :param adders 地址key
        :return:
        """
        try:
            return str(Loader.yamlFile(os.path.join(Route.getPath(self.global_dir),"blockette_path.yaml"))[adders])
        except Exception as e:
            self.logger.error("键值：%s未在%s中定义"%(adders,self.global_dir))

    def getAccunt(self,user):
        """
        获取用户组
        :param user:
        :return:
        """
        try:
            return Loader.yamlFile(os.path.join(Route.getPath(self.user_var_dir),"user.yaml"))[user]
        except Exception as e:
            self.logger.error("键值：%s没有在%s中定义"%(user,self.user_var_dir))

Env = Env()

if __name__ == '__main__':
    print(Env.getBlockeAdders("add_shop_cart"))
    Env.getBlockeAdders("错误Key")
    print(Env.getAccunt("ordinary_account"))

