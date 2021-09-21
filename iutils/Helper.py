# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Helper.py
# Author : YuYanQing
# Desc: 函数助手
# Date： 2021/8/5 17:05
'''
import re
import string
from faker import Factory
from iutils.Loader import Loader
from iutils.DateUtils import Moment
from iutils.IDCards import IdNumber
from iutils.RandUtils import RandValue
from iutils.EncryptUtils import CipherHelper
from testings.control.path import USER_VARS_PATH, GLOBAL_VAR_PATH

faker = Factory().create('zh_CN')
default_elements = string.ascii_letters + string.digits

def randInt(min_=1, max_=100):
    """
    随机生成整数
    :param min_:
    :param max_:
    :return:
    """
    return faker.random.randint(min_, max_)

def randFloat(min=0, max=1, length=2):
    """
    随机生成浮点数
    :param min:
    :param max:
    :param length:
    :return:
    """
    return RandValue.getFloat("{},{},{}".format(min, max, length))

def randTime(layout):
    """
    随机生成时间
    :return:
    """
    return str(Moment.getTime(layout))

def randComputeTime(days=0, seconds=0, microseconds=0,
                    milliseconds=0, minutes=0, hours=0, weeks=0, custom=None):
    """
    随机生成偏移时间
    :param days:
    :param seconds:
    :param microseconds:
    :param milliseconds:
    :param minutes:
    :param hours:
    :param weeks:
    :param custom:
    :return:
    """
    return str(Moment.computeDate(days=days, seconds=seconds, microseconds=microseconds,
                                  milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks, custom=custom))

def randLetters(length=10):
    """
    随机生成字母
    :param length:
    :return:
    """
    return ''.join(faker.random_letters(length=length))

def randSample(elements=default_elements, length=10):
    """
    随机生成字符（英文+数字）
    :param elements:
    :param length:
    :return:
    """
    return ''.join(faker.random_choices(elements=str(elements), length=length))

def randNumber():
    """
    随机生成手机号
    :return:
    """
    return faker.phone_number()

def randName():
    """
    随机生成名字
    :return:
    """
    return faker.name()

def randAddress():
    """
    随机生成所在地址
    :return:
    """
    return faker.address()

def randCountry():
    """
    随机生成国家名
    :return:
    """
    return faker.country()

def randCountryCode():
    """
    随机生成国家代码
    :return:
    """
    return ''.join(faker.country_code())

def randCityName():
    """
    随机生成城市名
    :return:
    """
    return faker.city_name()

def randCity():
    """
    随机生成城市
    :return:
    """
    return faker.city()

def randProvince():
    """
    随机生成省份
    :return:
    """
    return faker.province()

def randEmail():
    """
    随机生成email
    :return:
    """
    return faker.email()

def randIpv4():
    """
    随机生成IPV4地址
    :return:
    """
    return faker.ipv4()

def randLipate():
    """
    随机生成车牌号
    :return:
    """
    return faker.license_plate()

def randColor():
    """
    随机生成颜色
    :return:
    """
    return faker.rgb_color()

def randSafeHexColor():
    """
    随机生成16进制的颜色
    :return:
    """
    return faker.safe_hex_color()

def randColorName():
    """
    随机生成颜色名字
    :return:
    """
    return faker.color_name()

def randCompanyName():
    """
    随机生成公司名
    :return:
    """
    return faker.company()

def randJob():
    """
    随机生成工作岗位
    :return:
    """
    return faker.job()

def randPwd(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True):
    """
    随机生成密码
    :param lower_case:
    :param upper_case:
    :param digits:
    :param special_chars:
    :param length:
    :return:
    """
    return faker.password(length=length, special_chars=special_chars, digits=digits, upper_case=upper_case,
                          lower_case=lower_case)

def randUuid4():
    """
    随机生成uuid
    :return:
    """
    return faker.uuid4()

def randSha1(raw_output=False):
    """
    随机生成sha1
    :return:
    """
    return faker.sha1(raw_output=raw_output)

def randMd5(raw_output=False):
    """
    随机生成md5
    :return:
    """
    return faker.md5(raw_output=raw_output)

def randFemale():
    """
    随机生成女性名字
    :return:
    """
    return faker.name_female()

def randMale():
    """
    随机生成男性名字
    :return:
    """
    return faker.name_male()

def randUserInfo(sex=None):
    """
    随机生成粗略的基本信息
    :return:
    """
    return faker.simple_profile(sex=sex)

def randUserInfoPro(fields=None, sex=None):
    """
    随机生成详细的基本信息
    :return:
    """
    return faker.profile(fields=fields, sex=sex)

def randUserAgent():
    """
    随机生成浏览器头user_agent
    :return:
    """
    return faker.user_agent()

def randIdCard(random_sex):
    """
    随机生成有效身份证
    :return:
    """
    return IdNumber.getIDCard(random_sex)

def getUserVars(target_key=None):
    """
    组合静态跟动态变量
    :param target_key: 目标key
    :return:
    """
    user_vars = Loader.yamlFile(USER_VARS_PATH, False)
    if target_key is None:
        return combData(user_vars)
    else:
        _var = user_vars.get(target_key)
        return None if str(_var).title() in ["None", "Null"] else _var

def getExtractVars(target_key=None):
    """
    获取提取后的参数
    :param target_key: 目标key
    :return:
    """
    extract_vars = Loader.yamlFile(GLOBAL_VAR_PATH, False)
    if target_key is None:
        return extract_vars
    else:
        _var = extract_vars.get(target_key)
        return None if str(_var).title() in ["None", "Null"] else _var

def setEncryptVars(method,target_key):
    """
    给参数加密
    :param method: 加密风格 base64 md5 sha1
    :param target_key:
    :return:
    Example::
        >>> print(setEncryptVars("md5", "${randInt}"))
        >>> print(setEncryptVars("sha1", "$VAR_TEST_001"))
        >>> print(setEncryptVars("base64", "{{Custom_NULL_VAR}}"))
    """
    func_list = ["base64", "md5", "sha1"]
    if method in func_list:
        exec('_var = CipherHelper().{method}Encrypt("{target_key}")'.format(method=method, target_key=citeHelper(target_key)))
        var = locals()["_var"]
        return var.decode() if isinstance(var,bytes) else var
    else:
        raise ModuleNotFoundError("暂时仅支持：%s"%(", ".join(func_list)))

func_dict = {"Int": randInt,
               "Float": randFloat,
               "Time": randTime,
               "ComputeTime": randComputeTime,
               "Letters": randLetters,
               "Sample": randSample,
               "Number": randNumber,
               "Name": randName,
               "Address": randAddress,
               "Country": randCountry,
               "CountryCode": randCountryCode,
               "CityName": randCityName,
               "City": randCity,
               "Province": randProvince,
               "Email": randEmail,
               "Ipv4": randIpv4,
               "Lipate": randLipate,
               "Color": randColor,
               "SafeHexColor": randSafeHexColor,
               "ColorName": randColorName,
               "CompanyName": randCompanyName,
               "Job": randJob,
               "Pwd": randPwd,
               "Uuid4": randUuid4,
               "Sha1": randSha1,
               "Md5": randMd5,
               "Female": randFemale,
               "Male": randMale,
               "UserInfo": randUserInfo,
               "UserInfoPro": randUserInfoPro,
               "UserAgent": randUserAgent,
               "IdCard": randIdCard}

def citeHelper(name: str):
    """
    函数助手，输出以下常用随机数，返回结果值。支持的函数详情见func_dict:
    :param name:  函数名，需要在func_dict存在的key值
    :return:  随机函数调用结果 or None
    Example::
        >>> print(citeHelper('${randInt}'))
        >>> print(citeHelper('${randInt()}'))
        >>> print(citeHelper('${randLetters(5)}'))
        >>> print(citeHelper('${randSample(123567890,30)}'))
        >>> print(citeHelper("${getUserVars()}"))
        >>> print(citeHelper("${getUserVars(randPwd)}"))
        >>> print(citeHelper("{{UserAgent}}"))
        >>> print(citeHelper("{{Custom_None_VAR}}"))
        >>> print(citeHelper("{{Custom_NULL_VAR}}"))
        >>> print(citeHelper("$VAR_TEST_001"))
        >>> print(citeHelper('$ENC_(base64,Base64参数加密)'))
    """
    # fix: File "D:\Program Files\Python37\lib\re.py", line 173, in match
    # return _compile(pattern, flags).match(string)
    # TypeError: expected string or bytes-like object
    rand_vars = re.match("\$\{rand(.*)\((.*)\)\}", str(name))  # 带参数
    rand_no_vars = re.match("\$\{rand(.*)\}", str(name))  # 无参数
    dynamic_vars = re.match("\$\{get(.*)\((.*)\)\}", str(name))  # 动态自定义
    own_vars = re.match("\{\{(.*)\}\}", str(name))  # 动态自定义
    extract_vars = re.match("\$VAR_(.*)", str(name))  # 后置提取参数
    lock_vars = re.match("\$ENC_(.*)", str(name))  # 带参数
    pattern = rand_vars if rand_vars is not None else dynamic_vars
    if pattern is not None:
        key, value = pattern.groups()
        if func_dict.get(key):
            func = func_dict[key]
            _param = [eval(x) if x.strip().isdigit() else x for x in value.split(',')]
            if len(_param) >= 1 and "" not in _param:
                return func.__call__(*_param)
            elif "" in _param:
                return func.__call__()  # 没有带参数的
    elif own_vars is not None:
        return getUserVars(own_vars.group().strip("{}"))
    elif extract_vars is not None:
        return getExtractVars(extract_vars.group())
    elif rand_no_vars is not None:
        return func_dict[rand_no_vars.group().strip("${rand}")].__call__()
    elif lock_vars is not None:
        _lock_param = [eval(x) if x.strip().isdigit() else x for x in lock_vars.group().strip("$ENC_()").split(',')]
        if len(_lock_param) <2:
            raise IndexError(_lock_param)
        else:
            return setEncryptVars.__call__(*_lock_param)
    else:
        return name  # 函数名不存在返回原始值

def combData(dict_map: dict) -> dict:
    """
    合并参数化数据
    :param dict_map: 初始data dict类型
    举例 {"product": {"brand_id": "${randInt(1,2)}", "category_id": '${randFloat(1,2,3)}',"test": {"test": "${randSample(123567890abc,30)}"}}}
    转化后 {'product': {'brand_id': 7, 'category_id': 1.358, 'test': {'test': 'c071135252718592b58007a10093b6'}}}
    :return 转化后的数据 若无则返回原始值
    Example::
        >>> print(combData({"product": {"brand_id": "${randInt()}", "category_id": '${randFloat(1,2,3)}' }}))
        >>> print(combData({"create_time": "${randTime(10timestamp)}"}))
    """
    if isinstance(dict_map, dict):
        for key in list(dict_map.keys()):
            if isinstance(dict_map[key], list):
                for i in range(len(dict_map[key])):
                    dict_map[key][i] = combData(dict_map=dict_map[key][i])
            elif isinstance(dict_map[key], dict):
                dict_map[key] = combData(dict_map=dict_map[key])
            else:
                dict_map[key] = citeHelper(dict_map[key])
        return dict_map
    elif dict_map is None:  # fix：为空的时候raise 异常导致其它函数调用失败
        pass
    else:
        raise TypeError("传入的参数不是dict类型 %s" % (type(dict_map)))
