# -*- coding:utf-8 -*-
# Python version 2.7.16 or 3.7.6
'''
# FileName： OkHttps.py
# Author : YuYanQing
# Desc: request二次封装
# Date： 2021/6/6 0:37
'''
import sys
from typing import Dict, Text
from urllib.parse import unquote
sys.path.append('../')
import requests,allure
requests.packages.urllib3.disable_warnings()
from inside_utils.LogUtils import Logger
from requests_toolbelt import MultipartEncoder

class Httpx(object):
    def __init__(self):
        self.logger = Logger.writeLog()
        self.session = requests.session()
        self.params_method = ['get','head','patch','delete','options']
        self.data_method = ['post','put']

    def jsonToXwwwForm(self, post_data)->Text:
        """
        将origin dict转换为x-www-form-urlencoded
        Args:
            post_data (dict):{"a": 1, "b":2}
        Returns:
            str:a=1&b=2
        """
        if isinstance(post_data, dict):
            return "&".join(["{}={}".format(key, value) for key, value in post_data.items()])
        else:
            return post_data

    def xwwwFormToJson(self, post_data)->Dict:
        """
        将x-www-form-urlencoded转换为origin dict
        Args:
            post_data (str): a=1&b=2
        Returns:
            dict: {"a":1, "b":2}
        """
        if isinstance(post_data, str):
            converted_dict = {}
            for k_v in post_data.split("&"):
                try:
                    key, value = k_v.split("=")
                except ValueError:
                    raise Exception("Invalid x_www_form_urlencoded data format: {}".format(post_data))
                converted_dict[key] = unquote(value)
            return converted_dict
        else:
            return post_data

    def listToJson(self, origin_list)->Dict:
        """
        将list数据转化为json
        Args:
            origin_list (list)[{"name": "v", "value": "1"}, {"name": "w", "value": "2"}]
        Returns:
            dict:{"v": "1", "w": "2"}
        """
        return {item["name"]: item.get("value") for item in origin_list}

    def sendApi(self,method, url,
            params=None, data=None, headers:Dict=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None):
        """
        数据请求
        :param method: 请求方式
        :param url:  url地址
        :param params: (可选)在查询中发送的字典或字节
        :param data: (可选)字典，元组列表，字节或类文件
        :param headers: (可选)
        :param cookies: (可选)Dict或CookieJar对象发送
        :param files: (可选)Dictionary of ' " filename': file-like-objects ' '  用于多部分编码上传。
        :param auth: (可选)auth元组或可调用来启用   基本消化/定制HTTP身份验证。
        :param timeout: (可选)等待服务器发送的时间
        :param allow_redirects: (可选)默认为True
        :param proxies: 代理:(可选)字典映射协议或协议和主机名到代理的URL。
        :param hooks:
        :param stream: 是否立即下载响应 内容。 默认为“假”。
        :param verify: (可选)一个布尔值，它控制我们是否进行验证服务器的TLS证书，或字符串，在本地开发或测试期间可能有用。
        :param cert: (可选)if String, ssl客户端证书文件(.pem)的路径。  如果Tuple， ('cert'， 'key')对
        :param json:
        return Response <Response> 对象
        """
        req_info = {"method":method.lower(),"url":url,"headers":headers,"files":files,
                  "data":data,"json":json,"params":params,"auth":auth,
                  "cookies":cookies,"hooks":hooks,"proxies":proxies,"timeout":timeout}
        allure.attach(req_info)
        resp = self.session.request(method=method.lower(),url=url,headers=headers,data=data,json=json,
                                   params=params,auth=auth,cookies=cookies,hooks=hooks,proxies=proxies,timeout=timeout)
        return resp

    def uploadFile(self,method,url,file_path,data=None):
        """
        上传文件
        :param method:
        :param url:
        :param file_path:
        :param data:
        :return:
        """
        files = []
        if method == "single":
            files = {"file":open(file_path,"rb")}
            res = requests.post(url=url,files=files)
        elif method =="double" or method == "add_data":
            for i in range(len(file_path)):
                files.append(('file%s'%(i), (file_path[i], open(file_path[i], 'rb'))))
            res = self.sendApi(method="post",url=url, data=data, files=files)
        elif method == "stream":
            data = MultipartEncoder(fields=data)
            res = self.sendApi(method="post",url=url, data=data,headers={'Content-Type': data.content_type})
        return res.text

    def urlJoint(self,host,address)->Text:
        """
        拼接url
        :param host: 域名
        :param address: 地址
        :return:
        """
        return "%s%s"%(host,address)

    def getCookies(self,response,keyword):
        """
        获取cookies
        :param response
        :param keyword
        :return:
        """
        cookie_value = {}
        for key, value in response:
            cookie_value.update({keyword: value})
        return cookie_value

    def getUrl(self,response):
        """
        获取请求地址
        :param response:
        :return:
        """
        return response.url

    def getStatusCode(self,response):
        """
        获取返回的状态码
        :param response:
        :return:
        """
        return response.status_code

    def getResponseTime(self,response):
        """
        获取响应执行时间,单位s
        :param response:
        :return:
        """
        return response.elapsed.total_seconds()

    def getEncoding(self,response):
        """
        获取编码
        :param response:
        :return:
        """
        return response.apparent_encoding

    def getHttpxd(self,response):
        """
        获取请求方式
        :param response:
        :return:
        """
        return response.request

    def getText(self,response):
        """
        获取返回的text结果
        :param response:
        :return:
        """
        return response.text

    def getRaw(self, response):
        """
        获取返回的raw结果
        :param response:
        :return:
        """
        return response.raw

    def getReason(self,response):
        """
        获取请求状态
        :param response:
        :return:
        """
        return response.reason

    def getHeaders(self,response):
        """
        获取headers
        :param response:
        :return:
        """
        return response.headers

Httpx = Httpx()

if __name__ == '__main__':
    from BaseSetting import Route
    file_path =  Route.joinPath("debug","test_change_type.json")
    print(Httpx.uploadFile(url="https://yuyanqing.cn", file_path=file_path, method="single"))