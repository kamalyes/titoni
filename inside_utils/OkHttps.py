# -*- coding:utf-8 -*-
# Python version 2.7.16 or 3.7.6
'''
# FileName： OkHttps.py
# Author : YuYanQing
# Desc: request二次封装
# Date： 2021/6/6 0:37
'''
import sys
import json
import allure
import requests
sys.path.append('../')
from typing import Dict, Text
from requests_toolbelt import MultipartEncoder
requests.packages.urllib3.disable_warnings()
from inside_utils.LogUtils import Logger
from inside_utils.Initialize import Env
from inside_utils.AllureUtils import setTag

class Httpx(object):
    def __init__(self):
        self.logger = Logger.writeLog()
        self.session = requests.session()
        self.text_plain = ['get','head','patch','options']
        self.json_method = ['post','put','delete']

    def sendApi(self, method, url,
            params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None,animation=False,seesion=False):
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
        :param hookspip:
        :param stream: 是否立即下载响应 内容。 默认为“假”。
        :param verify: (可选)一个布尔值，它控制我们是否进行验证服务器的TLS证书，或字符串，在本地开发或测试期间可能有用。
        :param cert: (可选)if String, ssl客户端证书文件(.pem)的路径。  如果Tuple， ('cert'， 'key')对
        :param json:
        :param animation: 自动模式（需要传list）
        :param seesion 会话保持开关
        return Response <Response> 对象
        """
        if animation is True and data is not None:
            allures,headers,response = {}, {}, {}
            for index in range(len(data)):
                try:
                    for key in data[index].keys():
                        print(key)
                        if key == 'headers':
                            headers.update(data[index][key])
                        elif key == 'allures':
                            allures.update(data[index][key])
                        elif key == 'response':
                            response = data[index][key]
                        elif key == 'json':
                            params = data[index][key]
                except Exception as e:
                    pass
            # print(allures,headers,params,request,response,json)
            setTag(allures) # 打标签
        if method and url is not None:
            response = self.session.request(method=method.lower(), url=url, headers=headers,
                                            data=data, json=json, params=params, files=files, stream=stream, verify=verify,
                                            auth=auth, cookies=cookies, hooks=hooks, proxies=proxies, cert=cert,
                                            timeout=timeout)

            req_url = self.getUrl(response)
            req_raw = self.getRaw(response)
            req_text = self.getText(response)
            req_headers = self.getHeaders(response)
            req_encoding = self.getEncoding(response)
            req_httpxd = self.getHttpxd(response)
            req_reason = self.getReason(response)
            req_timeout = self.getResponseTime(response)
            [self.logger.info(index) for index in [req_url, req_httpxd, req_timeout,req_raw, req_text, req_headers, req_encoding, req_reason]]
            return response

            if seesion is True:
                self.closeSession()

    def closeSession(self):
        self.session.close()
        try:
            del self.session.cookies['JSESSIONID']
        except Exception:
            pass

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
        try:
            response_text = json.dumps(str(response.text), ensure_ascii=False, indent=4)
        except json.decoder.JSONDecodeError:  # only python3
            try:
                response_text = response.text
            except UnicodeEncodeError:
                # print(response.content.decode("utf-8","ignore").replace('\xa9', ''))
                response_text = response.content
        return response_text

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
    # print(Httpx.uploadFile(url="https://yuyanqing.cn", file_path=file_path, method="single"))
    print(Httpx.sendApi(url="http://localhost:8001/#network",method="post",headers={'Authorization': Env.getAuth()["Authorization"]}))
