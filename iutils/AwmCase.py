# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： ScanCase.py
# Author : YuYanQing
# Desc: 扫描用例
# Date： 2021/9/28 17:06
"""
import os
from iutils.Loader import Loader

def listDir(path, file_type: str, target_files: list = []):
    """
    列出xx文件目录下所有符合的类型文件绝对路径
    :param path:
    :param file_type:
    :param target_files:
    Example::
        >>> from BaseSetting import Route
        >>> scan_path = Route.getPath("test_yaml")
        >>> print(listDir(scan_path,"yaml"))
    """
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listDir(file_path, file_type, target_files)
        elif file_type.lower() == "csv":
            csv_data = Loader.csvFile(file_path)
            if csv_data:
                target_files.append(file_path)
        elif file_type.lower() == "yaml":
            yaml_data = Loader.yamlFile(file_path)
            if yaml_data is not None:
                target_files.append(file_path)
        elif file_type.lower() == "json":
            json_data = Loader.jsonFile(file_path)
            if json_data:
                target_files.append(file_path)
        else:
            if file_type.lower() == file_path.split(".")[-1]:
                target_files.append(file_path)

    return target_files
