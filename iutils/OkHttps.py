# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： OkHttps.py
# Author : YuYanQing
# Desc: request二次封装
# Date： 2021/6/6 0:37
"""
import os
import re
import json
import allure
import requests
import filetype
from uuid import uuid4
from typing import Text
from urllib import parse
from tlackback import *
from urllib.parse import urlparse
from requests_toolbelt import MultipartEncoder

requests.packages.urllib3.disable_warnings()
from BaseSetting import Route
from iutils.Loader import Loader
from iutils.LogUtils import Logger
from iutils.AllureUtils import setTag
from iutils.Processor import JsonPath
from iutils.Helper import combData
from iutils.Assertion import assertEqual
from iutils.DataKit import capitalToLower
# from testings.control.sql import connModel
from testings.control.variables import Global
from iutils.Exceptions import DependNotFoundError
from testings.control.path import DNS_PATH, ADDRESS_PATH  # 需对应的配置


class Httpx(object):
    def __init__(self):
        self.logger = Logger.writeLog()
        self.session = requests.session()
        self.text_plain = ['get', 'head', 'patch', 'options']
        self.json_method = ['post', 'put', 'delete']
        self.dns_pro = Loader.yamlFile(DNS_PATH)  # 域名配置
        self.address_pro = Loader.yamlFile(ADDRESS_PATH)  # url地址配置
        self.headers = Loader.yamlFile(os.path.join(Route.getPath("config"), "norm_headers.yaml"))

    def getShader(self, shader):
        """
        获取外部请求参数
        :param shader
        :return:
        """
        if isinstance(shader, dict):
            shader_keys = list(shader.keys())
            need_keys = ['path', 'file', 'method', 'var_key']
            fm = need_keys[1:3] == [item for item in shader_keys if item in need_keys[1:3]]
            fvm = need_keys[1:] == [item for item in shader_keys if item in need_keys[1:]]
            pfm = need_keys[0:3] == [item for item in shader_keys if item in need_keys[0:3]]
            pfvm = need_keys[0:] == [item for item in shader_keys if item in need_keys[0:]]
            path, file, method, var_key = shader.get("path"), shader.get("file"), shader.get("method"), shader.get(
                "var_key")
            if file and method:
                default_path = os.path.join(Route.getPath("test_yaml", True), file)
                if fm:
                    data_ = {"file_path": default_path, "method": method}
                if pfm:
                    file_path = os.path.join(Route.getPath(path, True), file)
                    data_ = {"file_path": file_path, "method": method}
                if fvm:
                    data_ = {"file_path": default_path, "var_key": var_key, "method": method}
                if pfvm:
                    file_path = os.path.join(Route.getPath(path, True), file)
                    data_ = {"file_path": file_path, "var_key": var_key, "method": method}
            else:
                raise Warning("最低必要参数为空：{}".format({"file": file, "method": method}))
            return {"argument": Loader.yamlFile(data_["file_path"])[data_.get("var_key")] if data_.get(
                "var_key") else Loader.yamlFile(data_["file_path"]),
                    "method": method}
        elif shader is None:
            return {}
        else:
            raise Warning("格式必须为Dict类型")

    def getData(self, data, allures=None, depends=None, tlackback=None, headers=None, demands=None, examines=None,
                extracts=None, dbs=None):
        """
        获取allures配置、headers、校验值
        :param data: config+子用例 list
        :param allures: allure报告配置
        :param depends: 用例依赖
        :param tlackback: 外部函数
        :param headers: 头部信息
        :param demands: 请求参数 例如：method及url
        :param examines: 校验值
        :param extracts: 提取参数值
        :param dbs: 数据库操作
        :return:
        Example::
            >>> single = {'headers': {'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip', 'accept-language': 'zh-CN,zh;q=0.9', 'content-type': 'application/json;charset=UTF-8', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}}
            >>> double = [[{'request': {'method': 'get', 'url': ['localhost', 8001]}}], {"depends":{"path": "test_helper.yaml", "test_case_name": "search_002"}},{'allures': {'severity': 'critical', 'description': '这是继承测试的用例描述', 'story': '引用后置处理后的变量&固定值'}, 'headers': {'accept': 'application/json, text/plain, */*', 'accept-encoding': 'gzip', 'accept-language': 'zh-CN,zh;q=0.9'}, 'request': {'method': 'get', 'url': ['localhost', 8001], 'params': {'Int': 1, 'ComputeTime': '2020-09-21 15:00', 'Letters': '$VAR_TEST_001', 'Sample': '$VAR_TEST_002'}}, 'validations': {'expected_code': 200, 'expected_content': {'code': 200, 'message': '', 'error': '', 'details': None}, 'expected_time': 10}}]
            >>> print(Httpx.getData(double, {}, {}, {}, {}, {}, {}, {}, {}))
        """
        if isinstance(data, list):
            for es in range(len(data)):
                if isinstance(data[es], list):
                    self.getData(data[es], allures, depends, tlackback, headers, demands, examines, extracts, dbs)
                elif isinstance(data[es], dict):
                    for key, value in data[es].items():
                        if key == 'headers':
                            headers.update(data[es][key])
                        elif key == 'request':
                            demands.update(data[es][key])
                        elif key == "tlackback":
                            tlackback = data[es][key]
                        elif key == 'depends':
                            if isinstance(data[es][key], dict):
                                depends = data[es][key]
                            elif isinstance(data[es][key], list) and len(data[es][key]) >= 2:
                                case_name = data[es][key][1]
                                depends.update(
                                    {"path": data[es][key][0], "case": [index for index in case_name.split(",")]})
                            else:
                                msg = "依赖性用例格式不正确Key：{}, Value：{}".format(key, data[es][key])
                                raise DependNotFoundError(msg)
                        elif key == 'allures':
                            allures.update(data[es][key])
                        elif key == 'validations':
                            examines = data[es][key]
                        elif key == "extract":
                            extracts = data[es][key]
                        elif key == "sql":
                            dbs = data[es][key]
        return allures, depends, tlackback, headers, demands, examines, extracts, dbs

    def saveData(self, enter_data, target_data):
        """
        存储变量
        :param enter_data 返回值
        :param target_data 对应的目标节点
        :return:
        Example::
            >>> enter_data = {"owner": [{"title": "The first title","description": "","url": ""},{"title": "The two title","description": ""}]}
            >>> target_data = {"test_001": ["$.owner[*].title",3]}
            >>> Httpx.saveData(enter_data=enter_data,target_data=target_data)
        """
        if isinstance(enter_data, dict):
            params = []
            for key, value in target_data.items():
                if (isinstance(value, list) and len(value) == 1) or isinstance(value, str):
                    _value = JsonPath.find(enter_data, value)
                    ivar = {"$VAR_%s" % (str(key).upper()): _value[0] if _value else None}
                elif isinstance(value, list) and (len(value) > 1) and (len(value) <= 2):
                    _value = JsonPath.find(enter_data, "{}".format(value[0]))
                    try:
                        ivar = {"$VAR_%s" % (str(key).upper()): _value[value[1]] if _value else None}
                    except IndexError:
                        raise IndexError("\n需提取的参数值：{}\n目前提取到{}个参数,\n参数值：{}".format(enter_data, len(_value), _value))
                Global.setValue(ivar)
                params.append(ivar)
            return params
        else:
            raise Warning("暂不支持该模式提取参数！！！")

    def dependFunc(self, yaml_path, case_name):
        """
        动态生成调用依赖性用例的方法
        :param yaml_path:
        :param case_name:
        :return:
        """
        return 'from iutils.OkHttps import Httpx\n' \
               'from testings.control.init import Envision\n' \
               'config = Envision.getYaml("{yaml_path}")["config"]\n' \
               'test_setup = Envision.getYaml("{yaml_path}")["test_setup"]\n' \
               'Httpx.sendApi(auto=True, esdata=[config, test_setup["{case_name}"]],allure_setup="前置操作-{case_name}")' \
            .format(yaml_path=yaml_path, case_name=case_name)

    def execDepend(self, depends):
        if isinstance(depends, dict):
            depend_path = depends.get("path")
            depend_cases = depends.get("case")
            for dp_case in depend_cases:
                self.logger.info("执行上级关联用例：{}".format((depend_path, dp_case)))
                dynamic_func = self.dependFunc(depend_path, dp_case)
                exec(dynamic_func)

    def sqlOperate(self, data, method="before", order="desc"):
        """
        数据库操作
        :param data  原始数据
        :param method: 执行先后
        :param order: 默认倒序从上之下执行，反之按事件的字母排列顺序执行（谨慎使用）
        Example::
            >>> data = {"before_call_sql_000": ['result', 'var_name', 'connModel.callSql', 'select * from promotion']}
            ... print(sqlOperate(data))
            ... params = {}
            ... val_value = ['var_name', 'connModel.callSql', 'select * from promotion']
            ... var_name, func, compound = val_value[0], val_value[1], val_value[2]
            ... exec("{var_name} = {func}(compound).to_dict()".format(var_name=var_name, func=func, compound=compound))
            ... params.update({val_value[1]:var_name})
            ... print(params)
        :return:
        """
        if isinstance(data, dict):
            valid_ext = {}
            invalid_ext = {}
            for ext_key, ext_value in data.items():
                if isinstance(ext_value, list) is True:
                    valid_ext.update({ext_key: ext_value})
                else:
                    invalid_ext.update({ext_key: ext_value})
            # 操作数据库
            if method in ["before", "after"]:
                if order == "asc":
                    # 按事件顺序执行
                    order_val = ",".join((lambda x: (x.sort(), x)[1])(list(valid_ext))).split(",")
                else:
                    order_val = ",".join((lambda x: (x, x)[1])(list(valid_ext))).split(",")
                for val_key in order_val:
                    val_value = valid_ext[val_key]
                    params = {}
                    if len(val_value) == 3:
                        var_name, func, compound = val_value[0], val_value[1], val_value[2]
                        loc = locals()
                        # 调用sql查询语句
                        exec("{var_name} = {func}(compound).to_dict()"
                             .format(var_name=var_name, func=func, compound=compound))
                        if "call_sql" in val_key:
                            params.update({val_value[1]: loc["var_name"]})
                        else:
                            raise TypeError("暂时仅支持doSql/callSql模式！")
                    else:
                        raise IndexError("数组长度越界！Key：%s, Value：%s" % (val_key, val_value))
                return params
            else:
                raise ModuleNotFoundError("暂时仅支持before/after模式！")
            # 错误的调用时raise异常
            if len(invalid_ext) > 0:
                raise TypeError("无效参数队列：%s " % (invalid_ext))

    def reqLog(self, **kwargs):
        """
        请求数据时的日志写入
        :return:
        """
        for key, value in kwargs.items():
            key = str(key).title().replace("_", "")
            self.logger.info("Request{} ==>> {}".format(key, json.dumps(value, indent=4, ensure_ascii=False)))

    def resLog(self, response):
        """
        接口响应数据
        :param response: 接口响应数据
        :return:
        """
        for key, value in response.items():
            if key in ["ResponseHeaders", "ResponseText"]:
                value = eval(str(value))
            elif key in ["ResponseHttpxd"]:
                value = str(value)
            self.logger.info("{} ==>> {}".format(key, json.dumps(value, indent=4, ensure_ascii=False)))

    def sendApi(self, method=None, url=None,
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None,
                esdata=None, auto=False, aided=False, seesion_=False,
                assert_data=None, hook_header=None, dbs=None, allure_setup=None, **kwargs):
        """
        数据请求
        :param method: 请求方式
        :param url:  url地址
        :param token:
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
        :param dbs:
        :param stream: 是否立即下载响应 内容。 默认为“假”。
        :param verify: (可选)一个布尔值，它控制我们是否进行验证服务器的TLS证书，或字符串，在本地开发或测试期间可能有用。
        :param cert: (可选)if String, ssl客户端证书文件(.pem)的路径。  如果Tuple， ('cert'， 'key')对
        :param json:
        :param esdata: 对接yaml中的config 基础数据
        :param auto: 全自动模式
        :param aided: 半自动
        :param assert_data: 手动效验
        :param hook_header 头部钩子 用于更新部分键值 （扩展）
        :param seesion_ 会话保持开关
        :param allure_setup: allure中的准备文案
        return Response <Response> 对象
        """
        if auto is True or aided is True:
            allures, depends, tracback, _headers, demands, examines, extracts, dbs = self.getData(esdata, {}, {}, {},
                                                                                                  {}, {}, {}, {}, {})
            if isinstance(demands, dict):  # 读取Yaml中request字段
                method = demands.get("method")
                # 根据dns+address 反转得到dns地址进行拼接为正确的url
                url = demands.get("url")
                timeout = demands.get("timeout")
                proxies = demands.get("proxies")
                allow_redirects = demands.get("allow_redirects")
                if isinstance(url, list) and len(url) == 2:
                    url = self.urlJoint(self.dns_pro.get(url[0]), self.address_pro.get(url[1]))
                elif isinstance(url, list) and len(url) == 1:
                    raise IndexError("自动模式下必须要先配置Host及Url或者仅传入Path，且为List例如：[host,url_path]")
                # 前置sql
                if dbs is not None:
                    self.sqlOperate(data)
                parameter = ["data", "json", "params", "shader"]
                loc = locals()
                for index in parameter:
                    exec('_{} = {}'.format(index, combData(demands.get(index))))
                data, json, params, shader = loc["_data"], loc["_json"], loc["_params"], loc["_shader"]
                # 处理其它yaml动态参数合并
                shader_argument, shader_method = self.getShader(shader).get("argument"), self.getShader(shader).get(
                    "method")
                comb_shader_argument = eval('{}'.format(combData(shader_argument)))
                if shader_method == "data":
                    data = comb_shader_argument
                elif shader_method == "json":
                    data = comb_shader_argument
                elif shader_method == "params":
                    params = comb_shader_argument
                    # if method == "get":  # 拦截不合法的数据
                    #     data = json = None
                    # else:
                    #     params = None
        else:
            allures, tracback, _headers, depends, examines, extracts, dbs = {}, {}, {}, {}, {}, {}, {}
        if depends:
            self.execDepend(depends)
        if tracback:
            for tb in tracback:
                try:
                    tb_result = eval(tb)
                except NameError:
                    tb_warn_msg = "tracback.py中找不到{tb}函数".format(tb=tb)
                    raise Warning(tb_warn_msg)
                with allure.step("函数引用"):
                    allure.attach(name="tracback--{tb}".format(tb=tb),
                                  body="{tb_result}".format(tb_result=str(tb_result)))
        setTag(allures)  # 打标签
        headers = dict(_headers if isinstance(_headers, dict) else {}, **headers if isinstance(headers, dict) else {})
        content_type = headers.get("content-type")
        method = method.lower() if method is not None else method
        if json is not None and content_type is None:
            headers.update(self.headers["json_headers"])
        elif params is not None and content_type is None:
            headers.update(self.headers["get_headers"])
        elif data is not None and content_type is None:
            headers.update(self.headers["from_headers"])
            if method == "get":
                data = parse.urlencode(data)
        elif method == "get" and content_type is None:
            headers.update(self.headers["get_headers"])
        elif method == "post" and content_type is None and json is not None:
            headers.update(self.headers["json_headers"])
        elif method == "post" and content_type is None and data is not None:
            headers.update(self.headers["from_headers"])
            if method == "get":
                data = parse.urlencode(data)
        elif content_type is not None:
            headers.update(self.headers["get_headers"])
        # fix requests.exceptions.InvalidHeader:
        # Value for header xxxx must be of type str or bytes, not <class 'int'>
        temp = {}
        for k in list(headers.keys()):
            temp.update({k.lower(): str(headers[k])})
        if hook_header is not None:
            [temp.update(capitalToLower(hd)) for hd in hook_header] \
                if isinstance(hook_header, list) else temp.update(
                hook_header)
        headers = combData(temp)
        with allure.step(
                "网络请求：{}".format(urlparse(url).path) if allure_setup is None else "{}：{}".format(allure_setup,
                                                                                                 urlparse(url).path)):
            allure.attach(name="Request Url", body=str(url))
            allure.attach(name="Request Method", body=str(method))
            allure.attach(name="Request Headers", body=str(headers))
            if params is not None:
                allure.attach(name="Query String Parametrize", body=str(params))
            elif data is not None:
                allure.attach(name="Query Data Parametrize", body=str(data))
            elif json is not None:
                allure.attach(name="Query Json Parametrize", body=str(json))
            elif examines is not None:
                allure.attach(name="Assert Parametrize", body=str(examines))
            elif assert_data is not None:
                allure.attach(name="Assert Parametrize", body=str(assert_data))
        self.reqLog(url=url, method=method, data=data, json_=json, params=params, headers=headers, files=files)
        if method not in self.text_plain + self.json_method:
            raise Exception("暂不支持：{}方式请求！！！".format(method))
        else:
            if re.match(r'^https?:/{2}\w.+$', url):
                pass
            else:
                raise Exception("%s-不是有效Url！！！" % (url))
            # 增加前置用例自动执行、效验等功能（与手动发送是一致的）
            # allure中已经注入了日志 若开启会产生三份雷同数据 debug也用不到、暂时补个位
            response = self.session.request(method=method, url=url, headers=headers,
                                            data=data, json=json, params=params, files=files, stream=stream,
                                            verify=verify,
                                            auth=auth, cookies=cookies, hooks=hooks, proxies=proxies, cert=cert,
                                            timeout=1 if timeout is None else int(timeout))
            req_code = self.getStatusCode(response)
            req_text = self.getText(response)
            req_headers = self.getHeaders(response)
            req_encoding = self.getEncoding(response)
            req_httpxd = self.getHttpxd(response)  # 获取请求方式，实际没有意义
            req_timeout = self.getResponseTime(response)
            req_content = self.getContent(response)
            req_reason = self.getReason(response)
            req_datas = {"ResponseCode": [req_code, self.getNotice(req_code)], "ResponseHttpxd": req_httpxd,
                         "ResponseReason": req_reason, "ResponseTime": req_timeout,
                         "ResponseEncoding": req_encoding, "ResponseHeaders": req_headers,
                         "ResponseContent": req_content, "ResponseText": req_text}
            self.resLog(req_datas)
            # 提取变量
            if req_content is not None and extracts is not None:
                self.saveData(req_content, extracts)
            with allure.step(
                    "响应结果：{}".format(urlparse(url).path) if allure_setup is None else "响应结果：{}".format(allure_setup)):
                {allure.attach(name="%s" % (str(key)), body=str(value).strip()) for key, value in req_datas.items()}
            # 部分值效验
            exp_variables = examines.get("expected_field", None)
            variables = {}
            if exp_variables is not None:
                for exp_key, exp_value in exp_variables.items():
                    _value = JsonPath.find(req_content, exp_key)
                    variables.update({exp_key: _value[0] if _value is not False else None})
            if examines != {} and assert_data is None:  # Yaml中声明了 但是case中没有声明
                assertEqual(validations=examines, code=req_code, reason=req_reason, content=req_content, text=req_text,
                            time=req_timeout, variables=variables)
            elif examines == {} and assert_data is not None:  # Yaml中未定义 但是case中声明
                assertEqual(validations=assert_data, code=req_code, reason=req_reason, content=req_content,
                            text=req_text,
                            time=req_timeout, variables=variables)
            elif examines != {} and assert_data is not None:  # 若二者都有则以最后定义的为主
                assertEqual(validations=assert_data, code=req_code, reason=req_reason, content=req_content,
                            text=req_text,
                            time=req_timeout, variables=variables)
            if seesion_ is True:
                self.closeSession()
            return response

    def closeSession(self):
        self.session.close()
        try:
            del self.session.cookies['JSESSIONID']
        except Exception:
            pass

    def setMultipartData(self, file_path):
        """
        重组流式上传文件的所需参数
        :return:
        """
        # 获取文件类型
        file_type = filetype.guess(file_path)
        mime_type = file_type.mime
        # 读取文件内容
        with open(file_path, 'rb') as file:
            file_handler = file.read()
        # 获取boundary
        boundary_value = uuid4().hex
        boundary = '--{0}'.format(boundary_value)
        # 组装文件
        fields = {"file": (os.path.basename(file_path), file_handler, mime_type)}
        encode_data = MultipartEncoder(fields, boundary)
        content_type = encode_data.content_type
        return encode_data, content_type

    def uploadFile(self, method, url, hook_header, file_path: list, data=None):
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
            data = self.setMultipartData(file_path)
            response = self.sendApi(method="post", url=url, hook_header=hook_header, headers={"content-type": data[1]},
                                    data=data[0])
        elif method == "double" or method == "add_data":
            for i in range(len(file_path)):
                files.append(('file%s' % (i), (file_path[i], open(file_path[i], 'rb'))))
                response = self.sendApi(method="post", url=url, hook_header=hook_header, files=files, data=data)
        return response

    def urlJoint(self, host, address) -> Text:
        """
        拼接url
        :param host: 域名
        :param address: 地址
        :return:
        """
        return parse.urljoin(host, address)

    def getCookies(self, response, keyword):
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

    def getUrl(self, response):
        """
        获取请求地址
        :param response:
        :return:
        """
        return response.url

    def getStatusCode(self, response):
        """
        获取返回的状态码
        :param response:
        :return:
        """
        return response.status_code

    def getResponseTime(self, response):
        """
        获取响应执行时间,单位s
        :param response:
        :return:
        """
        return response.elapsed.total_seconds()

    def getEncoding(self, response):
        """
        获取编码
        :param response:
        :return:
        """
        return response.apparent_encoding

    def getHttpxd(self, response):
        """
        获取请求方式
        :param response:
        :return:
        """
        return response.request

    def getText(self, response):
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

    def getContent(self, response):
        """
        获取Content
        :param response:
        :return:
        """
        try:
            return json.loads(response.content)
        except json.decoder.JSONDecodeError:
            return None

    def getRaw(self, response):
        """
        获取返回的raw结果
        :param response:
        :return:
        """
        return response.raw

    def getReason(self, response):
        """
        获取请求状态
        :param response:
        :return:
        """
        return response.reason

    def getHeaders(self, response):
        """
        获取headers
        :param response:
        :return:
        """
        return response.headers

    def getNotice(self, code=None):
        """
        根据穿过来的status_code返回相应的文案
        :param code:
        :return:
        """
        msg = {
            200: "OK：请求已正常处理",
            201: "(已创建)请求成功并且服务器创建了新的资源",
            202: "(已接受)服务器已接受请求，但尚未处理",
            203: "(非授权信息)服务器已成功处理了请求，但返回的信息可能来自另一来源",
            204: "No Content：请求处理成功，但没有任何资源可以返回给客户端",
            205: "(重置内容)服务器成功处理了请求，但没有返回任何内容。此响应要求请求者重置文档视图(例如，清除表单内容以输入新内容)",
            206: "Partial Content：是对资源某一部分的请求",
            301: "Moved Permanently：永久重定向",
            302: "Found：临时重定向",
            303: "See Other：资源的URI已更新，你是否能临时按新的URI访问",
            304: "Not Modified：本地资源已找到，但未符合条件请求",
            305: "(使用代理)请求者只能使用代理访问请求的网页",
            307: "Temporary Redirect：临时重定向。与302有相同的含义",
            400: "Bad Request：服务器端无法理解客户端发送的请求",
            401: "Unauthorized：(未授权)请求要求（BASIC认证，DIGEST认证）的认证信息,",
            403: "Forbidden：不允许访问那个资源",
            404: "Not Found：服务器上没有请求的资源。路径错误等",
            405: "(方法禁用)禁用请求中指定的方法",
            406: "(不接受)无法使用请求的内容特性响应请求的网页",
            407: "(需要代理授权)此状态码与 401(未授权)类似",
            408: "(请求超时)服务器等候请求时发生超时",
            409: "(冲突)服务器在完成请求时发生冲突",
            410: "(已删除)如果请求的资源已永久删除",
            411: "(需要有效长度)服务器不接受不含有效内容长度标头字段的请求",
            412: "(未满足前提条件)服务器未满足请求者在请求中设置的其中一个前提条件",
            413: "(请求实体过大)服务器无法处理请求，因为请求实体过大，超出服务器的处理能力",
            414: "(请求的 URI 过长)请求的 URI(通常为网址)过长，服务器无法处理",
            415: "(不支持的媒体类型)请求的格式不受请求页面的支持",
            416: "(请求范围不符合要求)如果页面无法提供请求的范围，则服务器会返回此状态码",
            417: "(未满足期望值)服务器未满足期望,请求标头字段的要求",
            500: "Internal Server Error：服务器端在执行请求时发生了错误",
            501: "(尚未实施)服务器不具备完成请求的功能。例如，服务器无法识别请求方法时可能会返回此代码",
            502: "(错误网关)服务器作为网关或代理，从上游服务器收到无效响应",
            503: "Service Unavailable：服务器暂时处于超负载或正在进行停机维护",
            504: "(网关超时)服务器作为网关或代理，但是没有及时从上游服务器收到请求",
            505: "(HTTP 版本不受支持)服务器不支持请求中所用的 HTTP 协议版本"
        }
        return msg.get(int(code), "暂没有录入这个状态，需进行添加")


Httpx = Httpx()
