# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AllureUtils.py
# Author : YuYanQing
# Desc: allure 标签
# Date： 2021/8/2 12:56
'''
import os
import allure
import shutil
from BaseSetting import Route

allure_result = Route.getPath("allure_result")
allure_report = Route.getPath("allure_report")

def setTag(data):
    """
    设置allure标签
    :param severity:  优先级
    :param epic:      史诗级
    :param feature:   一级标签 用于描述被测试产品需求
    :param story:     二级标签 用于描述feature的用户场景，即测试需求
    :param title:     标题 用于描述用例名称
    :param description:  备注信息
    Example::
        >>> setTag({'feature': '一级标签', 'severity': 'blocker'})
        >>> setTag([{'feature': '一级标签', 'severity': 'blocker'}, {'severity': 'critical（覆盖掉原有的blocker）', 'description': '这是用例描述', 'story': '正常创建三个平台货号的商品'}])
    :return:
    """
    if isinstance(data, list):
        data = {k: v for d in data for k, v in d.items()}
    for key, value in data.items():
        if key == 'story':
            allure.dynamic.story(value)
        elif key == 'feature':
            allure.dynamic.feature(value)
        elif key == 'title':
            allure.dynamic.title(value)
        elif key == 'severity':
            allure.dynamic.severity(value)
        elif key == 'description':
            allure.dynamic.description(value)

def delOldResult():
    if os.path.exists(allure_result):
        shutil.rmtree(allure_result)

def copyHistory():
    # 复制history文件夹，在本地生成趋势图
    report_history_dir = os.path.join(allure_report, "history")
    if not os.path.exists(report_history_dir):
        os.makedirs(report_history_dir)
    result_history_dir = os.path.join(allure_result, "history")
    # 如果不存在则先创建文件夹
    if not os.path.exists(result_history_dir):
        os.makedirs(result_history_dir)
    for file in os.listdir(report_history_dir):
        shutil.copy(os.path.join(allure_report, "history", file), result_history_dir)

def runAllureServer():
    os.system("allure open {}".format(allure_report))
