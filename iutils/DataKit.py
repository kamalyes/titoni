# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
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
'''
import json

def getTargetValue(dict_map: dict, separat: str = "$.", result_list:list={}):
    """
    递归获取所有的TargetValue
    :param dict_map: 初始data dict类型
    :param separat: 临时节点 str类型
    :param result_list:  用于存储所有遍历出来的结果 list集合
    :return: {xx,xx,xx} 以字典形式追加
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

def conversType(dict_map:dict,disable_data:list=[]) -> dict:
    """
    将只有数字的键值给强转类型为int
    :param dict_map: 初始data dict类型
    :param disable: 不用处理的键值对
    枚举 {'product': {'brand_id': None, 'category_id': '15888'} 转化后 {'product': {'brand_id': null, 'category_id': 15888}
    """
    if isinstance(dict_map, dict):
        for key in list(dict_map.keys()):
            if isinstance(dict_map[key], list):
                for i in range(len(dict_map[key])):
                    dict_map[key][i] = conversType(dict_map=dict_map[key][i],disable_data=disable_data)
            elif isinstance(dict_map[key], dict):
                dict_map[key] = conversType(dict_map=dict_map[key],disable_data=disable_data)
            elif str(dict_map[key]).isdigit() and str(key) not in disable_data:
                dict_map[key] = int(dict_map[key])
            elif str(dict_map[key]) =="null": # 统一处理str无法转化None
                dict_map[key] =None
        return json.dumps(dict_map,ensure_ascii=False).replace('\\"','"').replace('"{',"{").replace('}"',"}") # 临时打个补丁 后续若报错则需再次做兼容
    else:
        raise TypeError("传入的参数不是dict类型 %s" % (type(dict_map)))

# TODO: 将{$.xx.xx[xx]:value,xx,xx}格式数据进行重组
def dataRegroup(old_data: dict, temp={}) ->dict:
    """
    重组数据
    :param old_data:
    :return:
    """
    if isinstance(old_data,dict):
        for k,v in old_data.items():
            print(k,v)
