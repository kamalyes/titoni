# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： Swagger.py
# Author : YuYanQing
# Desc: 将Swagger文档中所有的接口解析为Case
{
    "schemes": [],
    "swagger": "2.0",
    "info": {
        "description": "这里是描述",
        "title": "这里是标题",
        "contact": {},
        "version": "1.0"
    },
    "host": "10.1.1.242:11001",
    "basePath": "",
    "paths":,
    "definitions":
    }
# Date： 2021/7/27 12:37
"""
import json
from BaseSetting import Route
from iutils.OkHttps import Httpx
from iutils.Loader import Loader
from iutils.Processor import JsonPath


class AnalysisSwagger(object):

    def __init__(self, swagger_host: str = None):
        """
        设置初始变量

        :param swagger_host
        """
        print("""
             _____      ____ _  __ _  __ _  ___ _ __
            / __\ \ /\ / / _` |/ _` |/ _` |/ _ \ '__|
            \__ \\ V  V / (_| | (_| | (_| |  __/ |
            |___/ \_/\_/ \__,_|\__, |\__, |\___|_|
                               |___/ |___/
        """)
        # swagger_url = swagger_host+"/swagger/doc.json" if isinstance(swagger_host,str) else "http://10.1.1.248:11001"+"/swagger/doc.json"
        # res = json.loads(Httpx.sendApi(method="get",url=str(swagger_url)).content.decode('UTF-8'))
        # Loader.writeJson(res, '../debug/swagger-api.json')
        # return res
        self.interface = {}  # json接口测试用例类型
        self.case_list = []  # 测试用例名称
        self.tags_list = []  # 测试模块标签
        # 定义测试用例集格式
        self.http_suite = {"config": {"name": "", "base_url": "", "variables": {}},
                           "testcases": []}
        # 定义测试用例格式
        self.http_testcase = {"name": "", "testcase": "", "variables": {}}
        res = Loader.jsonFile(Route.joinPath("debug", "swagger-api.json"))
        print(res)
        self.data = res['paths']  # 取接口地址返回的path数据,包括了请求的路径
        self.basePath = res['basePath']  # 获取接口的根路径
        # 第一错，swagger文档是ip地址，使用https协议会错误,注意接口地址的请求协议
        self.url = 'http://' + res['host']
        self.title = res['info']['title']  # 获取接口的标题
        self.http_suite['config']['name'] = self.title  # 在初始化用例集字典更新值
        self.http_suite['config']['base_url'] = self.url  # 全局url
        self.definitions = res['definitions']  # body参数

    def cleanPath(self):
        """
        清洗Path
        :return:
        """
        pass


if __name__ == '__main__':
    AnalysisSwagger().cleanPath()
