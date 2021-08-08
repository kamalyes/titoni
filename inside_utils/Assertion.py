# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Assertion.py
# Author : YuYanQing
# Desc: 效验结果集
# Date： 2021/3/27 18:05
'''

import sys
import allure
sys.path.append('../')
from inside_utils.LogUtils import Logger
logger = Logger.writeLog()

def less(a, b):
    "Same as a < b."
    return a < b

def less_or_equal(a, b):
    "Same as a <= b."
    return a <= b

def equal(a, b):
    "Same as a == b."
    return a == b

def unequal(a, b):
    "Same as a != b."
    return a != b

def greater(a, b):
    "Same as a > b."
    return a > b

def greater_or_equal(a, b):
    "Same as a >= b."
    return a >= b

def assertEqual(validations, code=None, time=None, content=None, text=None, variables=None):
    """
    校验测试结果
    :param validations: 效验值 dict
    :param text: 文本值
    :param code: 接口状态码
    :param time: 响应时间
    :param content: 返回的接口json数据
    :param variables: 部分字段效验
    :return:
    备注 有局限 若多重效验后者不会执行 程序直接跳出
    """
    if isinstance(validations,dict):
        with allure.step("接口常规值效验"):
            for key, value in validations.items():
                if "expected_code" == key and code is not None:
                    allure.attach(name="Assert Code", body="预期Code：{}，实际Code：{}".format(str(value),str(code)))
                    if int(code) != value:
                        raise AssertionError("接口状态码错误！\n %s != %s" % (code, value))

                elif "expected_time" == key and time is not None:
                    allure.attach(name="Assert Time", body="预期Time：{}，实际Time：{}".format(str(value),str(time)))
                    if int(time) != value:
                        raise AssertionError("接口响应时间不匹配！\n %s != %s" % (time, value))

                elif "expected_text" == key and text is not None:
                    allure.attach(name="Assert Text", body="预期Text：{}，实际Text：{}".format(str(value),str(text).strip()))
                    if str(text) != value:
                        raise AssertionError("接口响应文本值不匹配！\n %s != %s" % (text, value))

                elif "expected_content" == key and content is not None:
                    allure.attach(name="Assert Content", body="预期Content：{}，实际Content：{}".format(str(value),str(content).strip()))
                    if int(content) != value:
                        raise AssertionError("接口响应流式结果不匹配！\n %s != %s" % (content, value))

                elif "expected_variables" == key and variables is not None:
                    allure.attach(name="Assert Variables", body="预期Variables：{}，实际Variables：{}".format(str(value),str(variables).strip()))
                    if str(variables) != value:
                        raise AssertionError("接口响应部分文本值不匹配！\n %s != %s" % (variables, value))

if __name__ == '__main__':
    all = {'expected_code': 400, 'expected_content': {'code': 200, 'message': '', 'error': '', 'details': None}, 'expected_text': 'Bad Request', 'expected_time': 3, 'expected_variables': [{'$.variables1': 'value1'}, {'$.variables2': 'value2'}]}
    only_code = {'expected_code': 400}
    only_content = {'expected_content': {'code': 200, 'message': '', 'error': '', 'details': None}}
    code_and_content = {'expected_code': 400,'expected_content': {'code': 200, 'message': '', 'error': '', 'details': None}}
    assertEqual(all,code=200,text="Bad Request")
    assertEqual(only_code,code=200)
    assertEqual(code_and_content)