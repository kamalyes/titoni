# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Assertion.py
# Author : YuYanQing
# Desc: 效验结果集
# Date： 2021/3/27 18:05
'''
import re
import allure
from jsonschema import validate
from iutils.Helper import combData
from typing import Text, Any, Union

def numMatch(method, actual_value: Union[int, float], expect_value: Union[int, float], message: Text = ""):
    """
    number比较
    :param method: 方式
    :param actual_value: 实际值
    :param expect_value: 预期值
    :param message:
    :return:
    """
    actual_value, expect_value = float(actual_value), float(expect_value)
    if method == "equal":
        assert actual_value == expect_value, message
    elif method == "greaterThan":
        assert actual_value > expect_value, message
    elif method == "lessThan":
        assert actual_value < expect_value, message
    elif method == "greaterOrEqual":
        assert actual_value >= expect_value, message
    elif method == "lessOrEqual":
        assert actual_value <= expect_value, message
    elif method == "notEqual":
        assert actual_value != expect_value, message

def strMatch(method, actual_value: Text, expect_value: Any, message: Text = ""):
    """
    字符串比较
    :param method: 方式
    :param actual_value: 实际值
    :param expect_value: 预期值
    :param message:
    :return:
    """
    if method == "strEqual":
        assert str(actual_value) == str(expect_value), message
    elif method == "strExpInReality":
        assert isinstance(actual_value, (list, tuple, dict, str, bytes)), "actual_value type error"
        assert expect_value in actual_value, message
    elif method == "strRealityInExp":
        assert isinstance(expect_value, (list, tuple, dict, str, bytes)), "expect_value type error"
        assert actual_value in expect_value, message
    elif method == "strLength":
        assert len(actual_value) == len(expect_value), message

def typeMatch(actual_value: Any, expect_value: Any, message: Text = ""):
    """
    俩值类型比较
    :param actual_value:
    :param expect_value:
    :param message:
    :return:
    Example::
        >>> print(typeMatch("str", ["list"], "类型不正确"))
        >>> print(typeMatch(None, None, "类型不正确"))
    """
    assert type(actual_value) == type(expect_value), message

def startSwith(actual_value: Any, expect_value: Any, message: Text = ""):
    """
    实际值的开头等于预期
    :param actual_value:
    :param expect_value:
    :param message:
    :return:
    """
    assert str(actual_value).startswith(str(expect_value)), message

def endSwith(actual_value: Text, expect_value: Any, message: Text = ""):
    """
    实际值的结尾等于预期
    :param actual_value:
    :param expect_value:
    :param message:
    :return:
    """
    assert str(actual_value).endswith(str(expect_value)), message

def legalValues(contrast: Text):
    """
    标准化函数
    :param contrast:
    :return:
    Example::
        >>> print(legalValues("re"))
        >>> print(legalValues("equal"))
    """
    if contrast in ["eq", "equal", "=="]:
        return "equal"
    elif contrast in ["lt", "less_than", "lessThan", "<"]:
        return "lessThan"
    elif contrast in ["le", "less_or_equal", "lessOrEqual", "<=", "≤"]:
        return "lessOrEqual"
    elif contrast in ["gt", "greater_than", "greaterThan", ">"]:
        return "greaterThan"
    elif contrast in ["ge", "greater_or_equal", "greaterOrEqual", ">=", "≥"]:
        return "greaterOrEqual"
    elif contrast in ["ne", "not_equal", "notEqual", "!=", "≠"]:
        return "notEqual"
    elif contrast in ["str_eq", "string_equal", "stringEqual"]:
        return "strEqual"
    elif contrast in ["str_lg", "str_length", "strLength"]:
        return "strLength"
    elif contrast in ["re", "regexMatch"]:
        return "regexMatch"
    elif contrast in ["bg", "beginSwith"]:
        return " beginSwith"
    elif contrast in ["end", "endSwith"]:
        return "endSwith"
    else:
        return contrast

def dimMethod(contrast: Text):
    """
    通过模糊值返回指定func及内部method
    :param contrast:
    :return:
    """
    method = legalValues(contrast)
    if method[:3] == "str":
        return ["strMatch", method]
    elif method in ["startSwith", "endSwith"]:
        return method
    elif method in ["equal", "lessThan", "lessOrEqual", "greaterThan", "greaterOrEqual", "notEqual"]:
        return ["numMatch", method]
    else:
        return method

def equalData(method, actual_value: Any, expect_value: Any, message: Text = ""):
    """
    :param method: 比较方式
    :param actual_value: 实际值
    :param expect_value: 预期值
    :param message: 错误信息
    :return:
    Example::
        >>> equalData(method="lt",actual_value="5",expect_value="6")
        >>> equalData(method="str_eq",actual_value="Test12356",expect_value="Test123568")
    """
    try:
        dim_method = dimMethod(method)
        if isinstance(dim_method, list):
            func, method = dim_method[0], dim_method[1]
            globals().get(func)(method, actual_value, expect_value, message)
        elif isinstance(dim_method, str):
            func = dim_method
            globals().get(func)(actual_value, expect_value, message)
    except AssertionError:
        raise AssertionError(message, "比较方式：%s%s" % (func + "-", method if 'func' in locals().keys() else ""), "预期值",
                             expect_value, "实际值", actual_value)
    except TypeError:
        raise TypeError("{}比较函数错误".format(func + "-" if 'func' in locals().keys() else "",
                        method if 'method' in locals().keys() else "")
                        if isinstance(dim_method, list) else "{}比较函数错误".format(
            func if 'func' in locals().keys() else ""))

def assertEqual(validations: dict, code=None, time=None, content=None, text=None, variables=None):
    """
    校验测试结果 （备注 有局限 若多重效验后者不会执行 程序直接跳出）
    :param validations: 预期效验值
    :param text: 实际文本值
    :param code: 实际接口状态码
    :param time: 实际响应时间
    :param content: 返回的接口json数据
    :param variables: 实际效验值结果
    :return:
    Example::
        >>> only_code = {'expected_code': 500}
        >>> only_content = {'expected_content': {'code': 200, 'message': '', 'error': '', 'details': None}}
        >>> code_and_content = {'expected_code': "500" ,'expected_content': {'code': "${randInt}", 'message': '$VAR_TEST_001', 'error': '', 'details': None}}
        >>> expected_variables = {"expected_variables":{'test_001': 500, "test002":["aaa",500]}}
        >>> assertEqual(only_code,code=500)
        >>> assertEqual(code_and_content, content={'code': 200}, code= 500)
        >>> assertEqual(expected_variables, variables= {'test_001': 500, "test002":[]})
    """
    if isinstance(validations, dict):
        with allure.step("接口常规值效验"):
            for key, value in combData(validations).items():
                if "expected_code" == key:
                    allure.attach(name="Assert StatusCode", body="预期Code：{}，实际Code：{}".format(str(value), str(code)))
                    if str(value) != str(code):
                        raise AssertionError("接口状态码错误！\n %s != %s" % (value, code))

                elif "expected_time" == key:
                    allure.attach(name="Assert ResponseTime",
                                  body="预期Time：{}s，实际Time：{}s".format(str(value), str(time)))
                    if value < time:
                        raise AssertionError("接口响应时间不匹配！\n %s < %s" % (value, time))

                elif "expected_text" == key:
                    allure.attach(name="Assert ResponseText", body="预期Text：{}，实际Text：{}".format(value, text))
                    if value != text:
                        raise AssertionError("接口响应文本值不匹配！\n %s != %s" % (value, text))

                elif "expected_content" == key:
                    allure.attach(name="Assert ResponseContent",
                                  body="预期Content：{}，实际Content：{}（Dict格式数据仅做参考详情信息可见ResponseText）".format(value,
                                                                                                          content))
                    if value != content:
                        raise AssertionError("接口响应流式结果不匹配！\n %s != %s" % (value, content))

                elif "expected_schema" == key:
                    allure.attach(name="Assert JsonSchema", body="Schema：{}，实际Instance：{}".format(value, content))
                    if isinstance(content, dict):
                        validate(instance=value, schema=content)
                    else:
                        raise Warning("实际Instance类型不正确，暂不支持该方式效验！")
                elif "expected_variables" == key:
                    if isinstance(value, dict):
                        for ep_key, ep_value in value.items():
                            try:
                                ac_value = variables[ep_key]
                            except KeyError:
                                pass
                            if isinstance(ep_value, list):
                                assert_method, ep_value = ep_value[0], ep_value[1]
                                allure.attach(name="Assert Single Params {}".format(ep_key),
                                              body="预期Variables：{}，实际Variables：{}".format(ep_value, ac_value))
                                equalData(method=assert_method, actual_value=ac_value, expect_value=ep_value,
                                          message="接口响应部分文本值对比异常")
                            elif isinstance(ep_value, list) is False:
                                allure.attach(name="Assert Single Params {}".format(ep_key),
                                              body="预期Variables：{}，实际Variables：{}".format(ep_value, ac_value))
                                if ac_value != ep_value:
                                    raise AssertionError(
                                        "接口响应部分文本值对比异常, 比较方式：strMatch-equal 预期Variables：{}，实际Variables：{}".format(
                                            ep_value, ac_value))
                    else:
                        raise Warning("接口响应部分文本值不是字典类型，请检查返回体是否为Json类型！\n %s" % (variables))
    else:
        raise Warning("请先检查效验入参是否为Dict类型！！！")


if __name__ == '__main__':
    result = {
        "code": 0,
        "name": "中国",
        "msg": "login success!",
        "password": "000038efc7edc7538d781b0775eeaa009cb65865",
        "username": "test"
    }
    schema = {
        "properties": {
            "code": {
                "description": "error code",
                "type": "integer"
            },
            "name": {
                "description": "name",
                "type": "string"
            },
            "msg":
                {
                    "description": "msg",
                    "type": "string"
                },
            "password":
                {
                    "description": "error password",
                    "maxLength": 20,
                    "pattern": "^[a-f0-9]{20}$",  # 正则校验a-f0-9的16进制，总长度20
                    "type": "string"
                }
        },
        "required": [
            "code", "name", "msg", "password"
        ]
    }
    assertEqual(validations={"expected_schema": result}, content=schema)
