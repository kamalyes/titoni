# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Exceptions.py
# Author : YuYanQing
# Desc: 自定义错误类
# Date： 2021/6/11 15:15
'''
import json

class MyBaseFailure(Exception):
    pass

class MyBaseError(Exception):
    pass

class FileFormatError(MyBaseError):
    pass

class NotFoundError(MyBaseError):
    pass

class CSVNotFound(NotFoundError):
    pass


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)