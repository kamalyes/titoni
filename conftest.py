# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： conftest.py
# Author : YuYanQing
# Desc: 夹具
# Date： 2021/7/6 0:37
"""
import os
import sys
import time
sys.path.append('./')
from BaseSetting import Route
from iutils.YamlUtils import YamlHandle

def pytest_terminal_summary(terminalreporter):
    '''收集测试结果'''
    total = terminalreporter._numcollected
    if not bool(terminalreporter.stats):
        raise "暂时没有有效用例或开启了代理！！"
    else:
        passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
        failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
        error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
        skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
        successful = len(terminalreporter.stats.get('passed', [])) / terminalreporter._numcollected * 100
        duration = time.time() - terminalreporter._sessionstarttime
        data = {"total": total, "passed": passed, "failed": failed, "error": error, "skipped": skipped,
                "successful": successful, "duration": duration}
        YamlHandle.writeOjb(os.path.join(Route.getPath("workspaces"), "summary.yaml"), data, "w")