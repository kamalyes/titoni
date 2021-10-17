# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： ScanCase.py
# Author : YuYanQing
# Desc: 扫描用例
# Date： 2021/9/28 17:06
"""
import os
from BaseSetting import Route
from iutils.Loader import Loader
from testings.control.init import Envision

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

def dynamicExec(case_file,case_name):
    """
    动态执行测试用例
    :param case_name:
    :param case_file:
    :return:
    Example::
        >>> print(dynamicExec("test_helper.yaml","search_001"))
    """
    return "from iutils.OkHttps import Httpx\n" \
		   "from testings.control.init import Envision\n" \
		   "config = Envision.getYaml('{case_file}')['config']\n" \
		   "test_setup = Envision.getYaml('{case_file}')['test_setup']\n"\
           "class TestAutoExec:\n\t"\
           "def test_{case_name}(self):\n\t"\
           '\tHttpx.sendApi(auto=True, esdata=[config,test_setup["{case_name}"]])'.format(case_file=case_file,case_name=case_name)

def scanCase():
    """
    搜索自动执行的用例文件名及对应的用例名字
    :return:
    """
    case_list = []
    for file_path in listDir(Route.getPath("test_yaml"), "yaml"):
        case_list.append({os.path.split(file_path)[1]:[ts for ts in Envision.getYaml(os.path.split(file_path)[1])['test_setup']]})
    return case_list

def writeCase():
    """
    写入py文件
    :return:
    """
    for index in range(len(scanCase())):
        usecase = scanCase()[index]
        for key, value in usecase.items():
            for case in value:
                auto_exec = Route.getPath("auto_exec")
                if not os.path.exists(auto_exec):
                    os.makedirs(auto_exec)
                file_path = os.path.join(auto_exec, "{}_{}.py".format(str(key).replace(".yaml",""),case))
                with open(file_path, "w") as file:
                    file.writelines(dynamicExec(key, case))
                file.close()
