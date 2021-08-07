# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Helper.py
# Author : YuYanQing
# Desc: 函数助手
# Date： 2021/8/5 17:05
'''

import re
import faker
import string
faker =  faker.Faker()
default_elements = string.ascii_letters + string.digits

def randomRandint(min_=1, max_=100):
    return faker.random.randint(min_, max_)

def randomLetters(length=10):
    return ''.join(faker.random_letters(length=length))

def randomSample(elements=default_elements, length=10):
    return ''.join(faker.random_choices(elements=str(elements), length=length))

random_dict = {"Int": randomRandint, 'Letters': randomLetters, 'Sample': randomSample}

def randomHelp(name: str, pattern='\$\{Random(.*)\((.*)\)\}'):
    """
    随机函数助手，输出以下常用随机数，返回结果值。支持函数:
        1、randomRandint(min=1, max=100)    返回范围内整数，默认范围1～100
        2、randomLetters(length=10)         返回大小写字母组成的指定长度字符串，默认长度10
        3、randomSample(elements=string.letters+string.digits, length=10)   # 返回指定字符串，默认由大小写+数字组成，长度为10
    :param name:  函数名，需要在 randint、letters、sample 之间
    :param pattern:  匹配模式
    :return:  随机函数调用结果 or None
    """
    try:
        m = re.match(pattern, name)
        key, value = m.groups()
        if random_dict.get(key):
            func = random_dict[key]
            _param = [eval(x) if x.strip().isdigit() else x for x in value.split(',')]
            return func.__call__(*_param)
    except Exception as e:
        print(e)

def randData(dict_map:dict) -> dict:
    """
    随机数据
    :param dict_map: 初始data dict类型
    枚举 {"product": {"brand_id": None, "category_id": "${RandomInt(1,10)}","test":{"test001":"${RandomSample(123567890abc,30)}"}}}
    转化后 {'product': {'brand_id': None, 'category_id': 7, 'test': {'test001': '13091b396ab9012035a23cc6167025'}}}
    """
    if isinstance(dict_map, dict):
        for key in list(dict_map.keys()):
            if isinstance(dict_map[key], list):
                for i in range(len(dict_map[key])):
                    dict_map[key][i] = randData(dict_map=dict_map[key][i])
            elif isinstance(dict_map[key], dict):
                dict_map[key] = randData(dict_map=dict_map[key])
            else:
                dict_map[key] = randomHelp(dict_map[key])
        return dict_map
    else:
        raise TypeError("传入的参数不是dict类型 %s" % (type(dict_map)))

if __name__ == '__main__':
    print(randomHelp('${RandomInt(1,10)}'))
    print(randomHelp('${RandomLetters(5)}'))
    print(randomHelp('${RandomSample(123567890,30)}'))
    print(randomHelp('${RandomSample(123567890abc,30)}'))
    dict_map = {"product": {"brand_id": None, "category_id": "${RandomInt(1,10)}","test":{"test":"${RandomSample(123567890abc,30)}"}}}
    print(randData(dict_map))