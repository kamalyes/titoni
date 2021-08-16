# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： JsonUtils.py
# Author : YuYanQing
# Date： 2021/8/1 11:56
'''
import json
import difflib
import hashlib
from iutils.Loader import Loader
from iutils.LogUtils import Logger
logger = Logger.writeLog()

def wirteJson(target_data, file_path, method="w"):
    """
    写入Json
    :param target_data:
    :param file_path:
    :param method: 谨慎使用"a"追加模式（可能存在覆盖键值、json格式不对无法提取出来）
    :return:
    """
    with open(file_path, method, encoding="utf-8") as file:
        json.dump(target_data, file, ensure_ascii=False, indent=4)

def diffJson(filename1, filename2, targetPath):
    """
    比较两个文件内容的md5值；比较两个文件并输出到html文件中
    :param filename1:
    :param filename2:
    :param targetPath:
    :return:
    """
    file1Md5 = hashlib.md5.new(filename1.read()).digest()
    file2Md5 = hashlib.md5.new(filename2.read()).digest()
    if file1Md5 != file2Md5:
        text1_lines = Loader.jsonFile(filename1)
        text2_lines = Loader.jsonFile(filename2)
        d = difflib.HtmlDiff()
        # context=True时只显示差异的上下文，默认显示5行，由numlines参数控制，context=False显示全文，差异部分颜色高亮，默认为显示全文
        result = d.make_file(
            text1_lines, text2_lines, filename1, filename2, context=True)
        # 内容保存到result.html文件中
        try:
            with open(targetPath, 'a', encoding='utf-8') as result_file:
                result_file.write(result)
        except Exception as e:
            logger.error("写入文件失败:" + e)

def isJsonFormat(raw_msg):
    """
    用于判断一个字符串是否符合Json格式
    :param raw_msg:
    :return:
    """
    if isinstance(raw_msg,str):
        try:
            json.loads(raw_msg,encoding='utf-8')
        except ValueError:
            return False
        else:
            return True
    else:
        return False

def jsonToDict(target_data):
    """
    Json转字典
    :param target_data: 数据来源
    :return:
    """
    return json.loads(target_data)

def dictToJson(target_data):
    """
    字典转Json
    :param target_data: 数据来源
    :return:
    """
    return json.dumps(target_data,ensure_ascii=False,separators=(',', ': '))