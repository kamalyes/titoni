# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： DataKit.py
# Author : YuYanQing
# Desc: 处理Json及dict中转义的问题
# Date： 2021/7/17 19:05
+-------------------+---------------+
| Python            | JSON          |
+===================+===============+
| dict              | object        |
+-------------------+---------------+
| list, tuple       | array         |
+-------------------+---------------+
| str               | string        |
+-------------------+---------------+
| int, float        | number        |
+-------------------+---------------+
| True              | true          |
+-------------------+---------------+
| False             | false         |
+-------------------+---------------+
| None              | null          |
+-------------------+---------------+
"""
import json
from urllib.parse import unquote


def getTargetValue(dict_map: dict, separat: str = "$.", result_list: list = {}):
    """
    递归获取所有的TargetValue
    :param dict_map: 初始data dict类型
    :param separat: 临时节点 str类型
    :param result_list:  用于存储所有遍历出来的结果 list集合
    :return: {xx,xx,xx} 以字典形式追加
    Example::
        >>> print(getTargetValue(dict_map={"TEST_001": "TEST_VALUE001","TEST_002": [{"TEST_VALUE002-001": "VALUE"}, {"TEST_VALUE002-002": "VALUE"}]}))
    """
    if isinstance(dict_map, dict):
        for key, value in dict_map.items():
            temp = separat + key + "."
            # 若类型为list 后面还有一维或二位数组类型数据递归找
            if isinstance(value, list):
                for i in range(len(value)):
                    getTargetValue(dict_map=value[i], separat=temp + str(i) + ".")
            # 若类型还是dict，继续遍历
            elif isinstance(value, dict):
                getTargetValue(dict_map=value, separat=temp)
            # str或者int类型时就基本上判定为具体的xxx值
            elif str(value).isdigit():
                result_list.update({separat + key: int(value)})
            elif isinstance(value, str):
                result_list.update({separat + key: value})
        return result_list
    else:
        raise TypeError("传入的参数不是dict类型 %s" % (type(dict_map)))


def conversType(dict_map: dict, disable_data: list = []) -> dict:
    """
    将只有数字的键值给强转类型为int
    :param dict_map: 初始data dict类型
    :param disable: 不用处理的键值对
    Example::
        >>> print(conversType({'product': {'brand_id': None, 'category_id': '15888'}}))
        >>> print(conversType({'product': {'brand_id': None, 'category_id': '15888'}},["category_id"]))
    """
    if isinstance(dict_map, dict):
        for key in list(dict_map.keys()):
            if isinstance(dict_map[key], list):
                for i in range(len(dict_map[key])):
                    dict_map[key][i] = conversType(dict_map=dict_map[key][i], disable_data=disable_data)
            elif isinstance(dict_map[key], dict):
                dict_map[key] = conversType(dict_map=dict_map[key], disable_data=disable_data)
            elif str(dict_map[key]).isdigit() and str(key) not in disable_data:
                dict_map[key] = int(dict_map[key])
            elif str(dict_map[key]) == "null":  # 统一处理str无法转化None
                dict_map[key] = None
        return json.dumps(dict_map, ensure_ascii=False).replace('\\"', '"').replace('"{', "{").replace('}"',"}")  # 临时打个补丁 后续若报错则需再次做兼容
    else:
        raise TypeError("传入的参数不是dict类型 %s" % (type(dict_map)))


def convertDictToXFrom(post_data):
    """
    字典转xwww-from格式
    :param post_data: dict {"a": 1, "b":2}
    :return: str: a=1&b=2
    """
    if isinstance(post_data, dict):
        return "&".join(["{}={}".format(key, value) for key, value in post_data.items()])
    else:
        return post_data

def convertXFormToDict(post_data):
    """
    x-www-from格式转字典
    :param post_data (str): a=1&b=2
    :return dict: {"a":1, "b":2}
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

def convertListToDict(origin_list):
    """
    list转dict
    :param origin_list: (list) [{"name": "v", "value": "1"},{"name": "w", "value": "2"}]
    :return: dict:{"v": "1", "w": "2"}
    """
    return {item["name"]: item.get("value") for item in origin_list}

def capitalToLower(dict_map):
    """
    dict中的key转换小写
    :param dict_map:
    :return:
    """
    new_dict = {}
    for key in list(dict_map.keys()):
        new_dict[key.lower()] = dict_map[key]
    return new_dict

def lowerToCapital(dict_map):
    """
    dict中的key转换大写
    :param dict_map:
    :return:
    """
    new_dict = {}
    for key in list(dict_map.keys()):
        new_dict[key.upper()] = dict_map[key]
    return new_dict