# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Shell.py
# Author : YuYanQing
# Desc: 封装执行shell语句方法
# Date： 2020/7/15 16:15
'''
import subprocess

class Shell:
    @staticmethod
    def invoke(cmd):
        output, errors = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        o = output.decode("utf-8")
        return o
