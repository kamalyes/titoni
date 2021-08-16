# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Loader.py
# Author : YuYanQing
# Desc: 加载文件
# Date： 2021/6/11 15:15
'''
import os
import sys
import csv
import json
import time
import yaml
from typing import Text, Dict, List
from iutils.FolderUtils import FileHander
from iutils.Exceptions import FileFormatError
try:
    # PyYAML version >= 5.1
    yaml.warnings({"YAMLLoadWarning": False})
except AttributeError:
    pass

class Loader(object):
    def yamlFile(self,file_path=None):
        """
        加载yaml文件(做特殊兼容处理、自动引入目录：test_json)
        :param file_path: 文件路径
        :return:
        """
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                file.close()
        if FileHander.readFileType(file_path) in (".yaml", ".yml"):
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file.read())

    def jsonFile(self,file_path=None) -> Dict:
        """
        加载json文件(做特殊兼容处理、自动引入目录：test_json)
        :param file_name: 文件名
        :param file_path: 文件路径
        :return:
        """
        try:
            with open(file_path, mode="rb") as data_file:
                json_content = json.load(data_file)
        except json.JSONDecodeError as ex:
            err_msg = "JSONDecodeError:\nfile: %s\nerror: %s"%(file_path,ex)

            raise FileFormatError(err_msg)
        return json_content

    def csvFile(self,file_path: Text=None) -> List[Dict]:
        """
        加载CSV文件(做特殊兼容处理、自动引入目录：test_json)
        :param csv_name：文件名
        :param file_path： 文件路径
        Examples:
            username,password
            test1,111111
            test2,222222
            test3,333333
            [
                {'username': 'test1', 'password': '111111'},
                {'username': 'test2', 'password': '222222'},
                {'username': 'test3', 'password': '333333'}
            ]
        :param csv_file:
        :return:
        """
        csv_content_list = []
        with open(file_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_content_list.append(row)
        return csv_content_list

    def jsonToYaml(self,json_file):
        """
        支持json格式转yaml
        """
        if json_file.endswith("json"):
            with open(json_file, "r") as pf:
                json_to_dict = json.loads(pf.read())
            yaml_file = json_file.replace(".json", ".yaml")
            with open(yaml_file, "w") as fp:
                yaml.safe_dump(json_to_dict, stream=fp, default_flow_style=False)
                print("json转yaml成功!!!")
        else:
            print("不是json结尾的文件!!!")

    def yamlToJson(self,yaml_file):
        """
        支持json格式转yaml
        """
        if yaml_file.endswith("yaml"):
            with open(yaml_file, "r") as pf:
                # 先将yaml转换为dict格式
                yaml_to_dict = yaml.load(pf, Loader=yaml.FullLoader)
                dict_to_json = json.dumps(yaml_to_dict, sort_keys=False, indent=4, separators=(',', ': '))
            json_file = yaml_file.replace(".yaml", ".json")
            with open(json_file, "w") as fp:
                fp.write(dict_to_json)
                print("yaml转json成功!!!")
        else:
            print("不是yaml结尾的文件!!!")

    def getKeys(self,data):
        """
        获取dict下所有的key,value
        :param data:
        :return: 元祖类型
        """
        keys = []
        [keys.append((k,v))  for k,v in data.items()]
        return keys

    def writeJson(self,data, json_path,method="w"):
        """
        把处理后的参数写入json文件
        :param res:
        :param json_path:
        :return:
        """
        if isinstance(data, dict) or isinstance(data, list):
            with open(json_path, method, encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)
            print('Interface Params Total：{} ,write to json file successfully!'.format(len(data)))
        else:
            print('\n:{} Params is not dict.\n'.format(self.writeJson.__name__))

    def progress(self,length=10, refresh_sec=0.1):
        """
        进度条
        :param length: 控制进度条长度
        :param refresh_sec: 控制进度条增长速度
        :return:
        """
        bar_length = length
        for percent in range(0, 101):
            hashes = '■' * int(percent / 100.0 * bar_length)
            spaces = ' ' * (bar_length - len(hashes))
            sys.stdout.write("\rProgress: [%s] %d%%" % (hashes + spaces, percent))
            sys.stdout.flush()
            time.sleep(refresh_sec)

Loader = Loader()

if __name__ == '__main__':
    from BaseSetting import Route
    yaml_data = Loader.yamlFile(Route.joinPath("test_yaml","boss_pronew.yaml"))
    json_data = Loader.jsonFile(Route.joinPath("debug","test_change_type.json"))
    csv_data = Loader.csvFile(Route.joinPath("test_csv","order_sn.csv"))
    print("%s\n%s\n%s"%(yaml_data,json_data,csv_data[0]))
