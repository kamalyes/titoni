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
sys.path.append("../")
from BaseSetting import Route
from iutils.Loader import Loader
from urllib.parse import urlparse
from iutils.LogUtils import Logger
from iutils.FolderUtils import FileHander
from testings.control.path import DNS_PATH, ADDRESS_PATH

class HarParser(object):
    def __init__(self):
        self.logger = Logger.writeLog()
        self.dns_pro = Loader.yamlFile(DNS_PATH)  # 域名配置
        self.address_pro = Loader.yamlFile(ADDRESS_PATH)  # url地址配置
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

    def joinUrl(self, dns, path):
        """
        拼接url
        :param dns:
        :param path:
        :return:
        """
        if self.dns_pro is not None and self.address_pro is not None:
            for dns_key, dns_value in self.dns_pro.items():
                _dns = dns_key if dns_value == dns else False
            for route_key, route_value in self.address_pro.items():
                _path = route_key if route_value == path else False
            if _dns and _path:
                return [_dns,_path]
            else:
                return False
        else:
            return False

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
        headers, case_data, post_data = {}, {}, {}
        # 获取头部信息
        har_request = data.get("request")
        har_url = har_request.get("url")
        _scheme, _netloc, _path = urlparse(har_url).scheme, urlparse(har_url).netloc, urlparse(har_url).path
        join_url = self.joinUrl("{}://{}".format(_scheme, _netloc), _path)
        har_method = har_request.get("method").lower()
        har_headers = har_request.get("headers")
        loc = locals()
        for index in ["params", "text", "queryString"]:
            if index == "queryString":
                exec('post_data.update({index} = har_request.get("{index}"))'.format(index=index))
            else:
                exec('post_data.update({index} = har_request.get("postData").get("{index}"))'.format(index=index))
        name = _path.replace("/", "_")
        for i in range(len(har_headers)):
            index = har_headers[i].get("name").lower()
            header_list = ["accept", "user-agent", "content-type", "accept-encoding",
                           "accept-language", "authorization"]
            if index in header_list:
                headers.update({index: har_headers[i].get("value")})
        # 获取响应后的信息
        response = data.get("response")
        statusCode = response.get("statusCode")
        statusText = response.get("statusText")
        content = response.get("content").get("text").encode("utf-8")
        if self.checkSuffix(har_url) is True:
            case_data.update({"config": [{"headers": headers}, {"allures": self.alluer_tags},
                                         {"request": {"method": har_method,
                                                      "url": join_url if join_url else  har_url}}],
                              "test_setup": {name: {"headers": "子级扩展头部信息（写法与父类一致）", "request": post_data,
                                                    "depend": '["xxx.yaml","case","**kwargs"] {"path":"xxx.yaml","case":"test_setup下的case_name"}',
                                                    "allures": "子级扩展allure配置（写法与父类一致）",
                                                    "validations": {"expected_time": data.get("time"),
                                                                    "expected_code": "${expected_code}",
                                                                    "expected_reason": "${expected_reason}",
                                                                    "expected_text": "${expected_text}",
                                                                    "expected_border": "[left, own, right]",
                                                                    "expected_content": "${expected_content}",
                                                                    "expected_field": [{"$.variables1": "value1"},
                                                                                           {"$.variables2": "value2"}],
                                                                    "expected_schema": "json_schema"},
                                                    "sql": {"before_call_sql": "", "before_do_sql": "",
                                                            "after_call_sql": "", "after_do_sql": ""},
                                                    "extract": [{"var_name001": "json_path"},
                                                                {"var_name002": "json_path"}]}}})
        return case_data

    def getHarInfo(self, data):
        """
        获取request传参的所有有效信息（不清理原始数据）
        :param data
        :return:
        """
        headers, case_data, post_data = {}, {}, {}
        # 获取头部信息
        har_request = data.get("request")
        har_url = har_request.get("url")
        _scheme, _netloc, _path = urlparse(har_url).scheme, urlparse(har_url).netloc, urlparse(har_url).path
        join_url = self.joinUrl("{}://{}".format(_scheme, _netloc), _path)
        har_method = har_request.get("method").lower()
        har_headers = har_request.get("headers")
        loc = locals()
        for index in ["params","text","queryString"]:
            if  index == "queryString":
                exec('post_data.update({index} = har_request.get("{index}"))'.format(index=index))
            else:
                exec('post_data.update({index} = har_request.get("postData").get("{index}"))'.format(index=index))
        name = _path.replace("/", "_")
        for i in range(len(har_headers)):
            index = har_headers[i].get("name").lower()
            header_list = ["accept", "user-agent", "content-type", "accept-encoding",
                           "accept-language", "authorization"]
            if index in header_list:
                headers.update({index: har_headers[i].get("value")})
        # 获取响应后的信息
        response = data.get("response")
        statusCode = response.get("statusCode")
        statusText = response.get("statusText")
        content = response.get("content").get("text").encode("utf-8")
        if self.checkSuffix(har_url) is True:
            case_data.update({"config": [{"headers": headers}, {"allures": self.alluer_tags},
                                      {"request": {"method": har_method, "url": join_url if join_url else  har_url}}],
                           "test_setup": {name: {"headers": "子级扩展头部信息（写法与父类一致）","request": post_data,
                                                 "depend": '["xxx.yaml","case","**kwargs"] {"path":"xxx.yaml","case":"test_setup下的case_name"}',
                                                 "allures": "子级扩展allure配置（写法与父类一致）",
                                                 "validations": {"expected_time": data.get("time"),
                                                                 "expected_code": statusCode,
                                                                 "expected_reason": statusText,
                                                                 "expected_text": str(eval(content)),
                                                                 "expected_border": "[left, own, right]",
                                                                 "expected_content": str(eval(content)),
                                                                 "expected_field": [{"$.variables1": "value1"},
                                                                                        {"$.variables2": "value2"}],
                                                                 "expected_schema": "json_schema"},
                                                 "sql": {"before_call_sql": "", "before_do_sql": "",
                                                         "after_call_sql": "", "after_do_sql": ""},
                                                 "extract": [{"var_name001": "json_path"},
                                                             {"var_name002": "json_path"}]}}})
        return case_data

    def writeFile(self, data, file_path, method):
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
        commonnd = sys.argv
        try:
            file_path = commonnd[1]
            out_type = commonnd[2]
        except IndexError:
            raise IndexError("Example: python HarToData.py [file_path] [out_put_type]")
        # file_path = input("Please enter the path of the HAR file to escape:")
        # out_type = input("Please enter the storage type you want to escape (JSON, YAML) :").lower()
        har_data = self.readHarDatas(file_path)
        har_entries = har_data.get("har_entries")
        for i in range(len(har_entries)):
            har_info = self.getHarInfo(har_entries[i])
            head, tail = os.path.split(file_path)
            out_path = Route.getPath("debug") if head is "" else head
            out_file = os.path.join(out_path,tail.replace(".har", ""))
            if os.path.exists(out_path) is False:
                os.makedirs(out_path)
            self.writeFile(har_info, r"%s.%s" % (out_file, out_type), out_type)

HarParser().run()