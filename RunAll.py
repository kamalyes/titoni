# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： RunAllCase.py
# Author : YuYanQing
# Desc: PyCharm
# Date： 2021/3/27 17:28
'''
import os,sys,time,pytest
sys.path.append('../')
from inside_utils.Shell import Shell
from inside_utils.LogUtils import Logger
from inside_utils.DateUtils import TimeUtil
from BaseSetting import Route

logger =Logger().writeLog()

if __name__ == '__main__':
    file = os.path.basename(sys.argv[0])
    try:
        logger.info("===========开始执行脚本(时间：%s===========)"%(TimeUtil().getTime("%Y-%m-%d %H:%M:%S")))
        pytest.main([Route.getPath("test_path"), "--alluredir", Route.getPath("allure_result")])
    except Exception as e:
        logger.error("脚本批量执行失败！", e)
    try:
        shell = Shell()
        logger.info("开始执行报告生成")
        shell.invoke('allure generate %s -o %s --clean' % (Route.getPath("allure_result"), Route.getPath("allure_report")))
        shell.invoke("allure open %s"%(Route.getPath("allure_report")))
    except Exception as e:
        logger.error("报告生成失败，请重新执行", e)
        raise
    time.sleep(5)
