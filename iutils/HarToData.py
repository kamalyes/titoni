# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： HarToData.py
# Author : YuYanQing
# Desc: Har数据包转换为Json或Yaml文件
# Date： 2021/6/11 15:01
'''
import io
import os
import sys
import yaml
import json
from urllib.parse import urlparse
from iutils.Loader import Loader
from iutils.LogUtils import Logger
from iutils.FolderUtils import FileHander

class HarParser(object):
    def __init__(self):
        self.logger = Logger.writeLog()
        self.alluer_tags = Loader.yamlFile(os.path.join("../config", "allure_feature.yaml"))

    def loadHarEntries(self, file_path):
        """
        加载har中entries信息
        :param file_path:
        :return:
        """
        with io.open(file_path, "r+", encoding="utf-8-sig") as f:
            try:
                content_json = json.loads(f.read())
                return content_json["log"]["entries"]
            except (KeyError, TypeError):
                self.logger.error("HAR file content error: {}".format(file_path))
                sys.exit(1)

    def readHarDatas(self, file_path):
        """
        读取Har文件并return dict类型的数据
        :param file_path 文件目录
        :return:
        """
        result = {}
        if FileHander.readFileType(file_path) == ".har":
            result.update({"har_entries": self.loadHarEntries(file_path)})
        else:
            raise "The file type must be in Har format"
        return result

    def checkSuffix(self, url):
        """
        检查是否为cgi服务还是html/woff2/css/js/png...资源
        :param data
        :param req_url_type url尾缀格式类型
        :param rule 过滤的类型
        :return:
        """
        url_type = str(url).split(".")[-1].lower()  # 取出尾缀并转换为小写格式
        rule = ["html", ".woff2", "font", "crx", "htm", "jsp", "css", "mp4", "avi", "png", "jpg", "ico", "js"]
        if url_type not in rule:
            return True
        else:
            print("暂时不支持%s格式" % (url_type))

    def setHarInfo(self, data):
        """
        设置request传参所需的字段
        :param data
        :return:
        """
        result, params = {}, {}
        request = data.get("request")
        method = request.get("method")
        headers = request.get("headers")
        httpVersion = request.get("httpVersion")
        # postData = request.get("postData", "post data is not exist")
        url = "${host}%s" % ('{uri.path}'.format(uri=urlparse(request.get("url"))))
        name = "%s" % ('{uri.path}'.format(uri=urlparse(request.get("url")))).replace("/", "")
        result.update({"case_name": "%s" % ('{uri.path}'.format(uri=urlparse(request.get("url")))).replace("/", "")})
        for i in range(len(headers)):
            index = headers[i].get("name").lower()
            header_list = ["accept", "user-agent", "content-type", "accept-encoding", "accept-language"]
            if index in header_list and index != "authorization" and index != "host":
                result.update({index: headers[i].get("value")})
            elif index in ["host", "authorization"]:
                result.update({index: "${%s}" % (index)})
            elif index == "referer":
                result.update({index: "${referer}%s" % ('{uri.path}'.format(uri=urlparse(headers[i].get("value"))))})
                # "request": {"file": "文件上传？（True or False）", "method": method, "url": url, "httpVersion": httpVersion,
                #             "cookies": None, "params": "${params}"}
        if self.checkSuffix(url) is True:
            params.update({"config": [{"headers": result}, {"allures": self.alluer_tags},
                                      {"request": {"method": method, "url": url}}],
                           "test_setup": {name: {"headers": result, "allures": self.alluer_tags,
                                                 "validations": {"expected_time": data.get("time"),
                                                                 "expected_code": "${expected_code}",
                                                                 "expected_text": "${expected_text}",
                                                                 "expected_content": "${expected_content}",
                                                                 "expected_variables": [{"$.variables1": "value1"},
                                                                                        {"$.variables2": "value2"}]},
                                                 "extract": [{"$.extract1": "value1"}, {"$.extract2": "value2"}]}}})
        return params

    def getHarInfo(self, data):
        """
        获取request传参的所有有效信息（不清理原始数据）
        :param data
        :return:
        """
        result, params = {}, {}
        # 获取头部信息
        request = data.get("request")
        url = request.get("url")
        method = request.get("method")
        httpVersion = request.get("httpVersion")
        headers = request.get("headers")
        name = "%s" % ('{uri.path}'.format(uri=urlparse(request.get("url")))).replace("/", "")
        for i in range(len(headers)):
            index = headers[i].get("name").lower()
            header_list = ["host", "accept", "user-agent", "content-type", "referer", "accept-encoding",
                           "accept-language", "authorization"]
            if index in header_list:
                result.update({index: headers[i].get("value")})
        # 获取响应后的信息
        response = data.get("response")
        statusCode = response.get("statusCode")
        statusText = response.get("statusText")
        content = response.get("content").get("text")
        # cookies = response.get("cookies","${cookies}")
        # "request": {"file": "文件上传？（True or False）", "method": method, "url": url, "httpVersion": httpVersion,
        #             "cookies": None, "params": "${params}"},
        if self.checkSuffix(url) is True:
            params.update({"config": [{"headers": result}, {"allures": self.alluer_tags},
                                      {"request": {"method": method, "url": url}}],
                           "test_setup": {name: {"headers": result, "allures": self.alluer_tags,
                                                 "validations": {"expected_time": data.get("time"),
                                                                 "expected_code": statusCode,
                                                                 "expected_text": statusText,
                                                                 "expected_content": str(content).strip(),
                                                                 "expected_variables": [{"$.variables1": "value1"},
                                                                                        {"$.variables2": "value2"}]},
                                                 "extract": [{"$.extract1": "value1"}, {"$.extract2": "value2"}]}}})
        return params

    def writeFile(self, data, file_path, method) -> str:
        """
        写入文件
        :param data:
        :param method 方式 --->json、yaml
        :return:
        """
        outpath = "%s.%s" % (file_path.split(".")[0], method)
        if method == "json":
            with open(outpath, "w", encoding="utf-8") as file:
                file.write(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            with open(outpath, "w", encoding="utf-8") as file:
                yaml.dump(data, file, default_flow_style=False, allow_unicode=True, indent=2)

    def run(self):
        """
        合并数据
        :return:
        """
        file_path = input("Please enter the path of the HAR file to escape:")
        type = input("Please enter the storage type you want to escape (JSON, YAML) :").lower()
        har_data = self.readHarDatas(file_path)
        har_entries = har_data.get("har_entries")
        for i in range(len(har_entries)):
            har_info = self.getHarInfo(har_entries[i])
            head, tail = os.path.split(file_path)
            self.writeFile(har_info, r"%s/%s.%s" % (head, tail.replace(".har", ""), type), type)


if __name__ == '__main__':
    HarParser().run()