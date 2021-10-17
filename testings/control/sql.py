# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： sql.py
# Author : YuYanQing
# Desc: SQL驱动连接
# Date： 2021/8/11 10:21
"""

from iutils.MySQLUtils import MysqlTools
from testings.control.data import APPLICATION

DB_HOST = APPLICATION["database"]["host"]
DB_PORT = APPLICATION["database"]["port"]
DB_USER = APPLICATION["database"]["user"]
DB_PASSWORD = APPLICATION["database"]["password"]
DB_NAME = APPLICATION["database"]["db_name"]
DB_CHARSET = APPLICATION["database"]["charset"]

connModel = MysqlTools(host=DB_HOST, user=DB_USER, pass_word=DB_PASSWORD, database=DB_NAME, port=DB_PORT)
connModel.init()