# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： CheckStatus.py
# Author : YuYanQing
# Desc: 根据穿过来的status_code返回相应的文案
# Date： 2020/10/21 17:57
'''
from utils.LogHander import Logger

class CodeWriting:
    def __init__(self):
        self.logger = Logger().writeLog()

    def notice(self,code=None):
        msg = {
            200 : "OK：请求已正常处理",
            201 : "(已创建)请求成功并且服务器创建了新的资源",
            202 : "(已接受)服务器已接受请求，但尚未处理",
            203 : "(非授权信息)服务器已成功处理了请求，但返回的信息可能来自另一来源",
            204 : "No Content：请求处理成功，但没有任何资源可以返回给客户端",
            205 : "(重置内容)服务器成功处理了请求，但没有返回任何内容。此响应要求请求者重置文档视图(例如，清除表单内容以输入新内容)",
            206 : "Partial Content：是对资源某一部分的请求",
            301 : "Moved Permanently：永久重定向",
            302 : "Found：临时重定向",
            303 : "See Other：资源的URI已更新，你是否能临时按新的URI访问",
            304 : "Not Modified：本地资源已找到，但未符合条件请求",
            305 : "(使用代理)请求者只能使用代理访问请求的网页",
            307 : "Temporary Redirect：临时重定向。与302有相同的含义",
            400 : "Bad Request：服务器端无法理解客户端发送的请求",
            401 : "Unauthorized：(未授权)请求要求（BASIC认证，DIGEST认证）的认证信息,",
            403 : "Forbidden：不允许访问那个资源",
            404 : "Not Found：服务器上没有请求的资源。路径错误等",
            405 : "(方法禁用)禁用请求中指定的方法",
            406 : "(不接受)无法使用请求的内容特性响应请求的网页",
            407 : "(需要代理授权)此状态码与 401(未授权)类似",
            408 : "(请求超时)服务器等候请求时发生超时",
            409 : "(冲突)服务器在完成请求时发生冲突",
            410 : "(已删除)如果请求的资源已永久删除",
            411 : "(需要有效长度)服务器不接受不含有效内容长度标头字段的请求",
            412 : "(未满足前提条件)服务器未满足请求者在请求中设置的其中一个前提条件",
            413 : "(请求实体过大)服务器无法处理请求，因为请求实体过大，超出服务器的处理能力",
            414 : "(请求的 URI 过长)请求的 URI(通常为网址)过长，服务器无法处理",
            415 : "(不支持的媒体类型)请求的格式不受请求页面的支持",
            416 : "(请求范围不符合要求)如果页面无法提供请求的范围，则服务器会返回此状态码",
            417 : "(未满足期望值)服务器未满足期望,请求标头字段的要求",
            500 : "Internal Server Error：服务器端在执行请求时发生了错误",
            501 : "(尚未实施)服务器不具备完成请求的功能。例如，服务器无法识别请求方法时可能会返回此代码",
            502 : "(错误网关)服务器作为网关或代理，从上游服务器收到无效响应",
            503 : "Service Unavailable：服务器暂时处于超负载或正在进行停机维护",
            504 : "(网关超时)服务器作为网关或代理，但是没有及时从上游服务器收到请求",
            505 : "(HTTP 版本不受支持)服务器不支持请求中所用的 HTTP 协议版本"
        }
        code = int(code)
        msg = msg.get(code, None)
        if code>=200 and code<300:
            self.logger.info("返回码：%s,基本信息：%s"%(code,msg))
        elif code >=300 and code<400:
            self.logger.warning("返回码：%s,警告信息：%s"%(code,msg))
        elif code >=400:
            self.logger.error("返回码：%s,错误信息：%s"%(code,msg))
        return msg

if __name__ == "__main__":
    for i in (200,301):
        CodeWriting().notice(i)