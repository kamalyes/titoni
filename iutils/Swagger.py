# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： Swagger.py
# Author : YuYanQing
# Desc:
# Date： 2022/2/17 10:15
"""
import re

import requests
from jsonschema import validate

from iutils.OkHttps import Httpx


class SwaggerMange:
    def __init__(self, swagger_docs_url):
        self.session = requests.session()
        self.swagger_docs_url = swagger_docs_url
        self.request_method = ['get', 'head', 'patch', 'options', 'post', 'put', 'delete']

    def loadSwaggerDocs(self):
        """
        加载swagger数据、标准的格式: https://swagger.io/docs/specification/basic-structure/
        :return:
        """
        if re.match(r'^https?:/{2}\w.+$', str(self.swagger_docs_url)):
            response = self.session.request(method="get", url=self.swagger_docs_url)
        schema_ = {
            "type": "object",
            "required": ["swagger", "host", "basePath", "paths", "definitions", "schemes"],
            "properties": {
                "swagger": {"type": "string"},
                "host": {"type": "string"},
                "basePath": {"type": "string"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"}},
                "paths": {
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
                "definitions": {
                    "type": "object",
                    "required": [],
                    "properties": {}
                },
                "schemes": {
                    "type": "array",
                    "required": [],
                    "properties": {}
                }
            }
        }
        res_content = Httpx.getContent(response)
        validate(instance=res_content, schema=schema_)
        return res_content

    def breakUpPath(self, data):
        """
        拆分path
        :param data:
        :return:
        """
        consumes = data.get("consumes", None)
        produces = data.get("produces", None)
        tags = data.get("tags", None)
        summary = data.get("summary", None)
        parameters = data.get("parameters", None)
        return consumes, produces, tags, summary, parameters

    def subApiInfo(self, swagger_data, grep_path=None, paths_name=None):
        """
        过滤并组合相关的接口信息
        :param paths_name:
        :param swagger_data:
        :param grep_path:
        :return:
        """
        for key, value in swagger_data.items():
            if "/" in key[0]:
                self.subApiInfo(swagger_data=value, paths_name=key)
            if key.lower() in self.request_method and not paths_name is None:
                consumes, produces, tags, summary, parameters = self.breakUpPath(value)
                # print(paths_name, key, consumes, produces, tags, summary, parameters)
            if key.lower() == "schema":
                definitions = value.get("$ref", None)
                print(definitions)
            if isinstance(value, dict):
                self.subApiInfo(swagger_data=value)
            # path = JsonPath.find(swagger_data, f"$.paths..{grep_path}")


if __name__ == '__main__':
    swagger_docs_url = "https://gateway.sit.rvet.cn/doctor-api/swagger/doc.json"
    swagger_mange = SwaggerMange(swagger_docs_url)
    swagger_docs = swagger_mange.loadSwaggerDocs()
    grep_path = "/doctor-api/area/list"
    # swagger_mange.subApiInfo(swagger_data=swagger_docs, grep_path=grep_path)
    swagger_mange.subApiInfo(swagger_data=swagger_docs)
