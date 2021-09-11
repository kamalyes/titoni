# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RunAllCase.py
# Author : YuYanQing
# Desc: PyCharm
# Date： 2021/3/27 17:28
'''
import os
import sys
import time
import pytest
from BaseSetting import Route
from iutils.Shell import Shell
from iutils.LogUtils import Logger
from iutils.DateUtils import Moment

if __name__ == '__main__':
    shell = Shell()
    Logger.deleteLog(30)
    path = Route.getPath("report_data")
    if os.path.exists(path):
        os.remove(path)
    logger = Logger.writeLog()
    currentTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    allure_result = Route.getPath("allure_result")
    allure_report = Route.getPath("allure_report")
    file = os.path.basename(sys.argv[0])
    try:
        logger.info("""
                                 _    _         _      _____         _
                      __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
                     / _` | '_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
                    | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
                     \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
                       |_|Starting Time %s
                    """ % (Moment.getTime("%Y-%m-%d %H:%M:%S")))
        # debug 模式下调用
        pytest.main([Route.getPath("test_path"), "--alluredir", allure_result,'-W','ignore:Module already imported:pytest.PytestWarning'])
        shell.invoke("allure generate {} -c -o {} --clean".format(allure_result, allure_report))
        shell.invoke("allure open %s" % (Route.getPath("allure_report")))
        # 生产模式调用
        # shell.invoke("python3 -m pytest -vs --alluredir  {}".format(allure_report))
    except Exception as e:
        logger.error("初始化脚本批量执行失败！", e)