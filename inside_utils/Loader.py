# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Loader.py
# Author : YuYanQing
# Desc: 加载文件
# Date： 2021/6/11 15:15
'''
import os,sys,csv,json,yaml

from inside_utils.JsonPath import JsonPath

sys.path.append('../')
from BaseSetting import Route
from typing import Text, Dict, List
from inside_utils.FileUtils import FileHander
from inside_utils.Exceptions import FileFormatError
try:
    # PyYAML version >= 5.1
    yaml.warnings({"YAMLLoadWarning": False})
except AttributeError:
    pass

class Loader():
    def yamlFile(self, file_name,file_path=None):
        """
        加载yaml文件(做特殊兼容处理、自动引入目录：test_data)
        :param file_name: 文件名
        :param file_path: 文件路径
        :return:
        """
        if file_path != None:
            yaml_file = os.path.join(file_path, file_name)
        else:
            yaml_file = os.path.join(Route.getPath("test_data"),file_name)
        try:
            if FileHander.readFileType(yaml_file) in(".yaml",".yml"):
                with open(yaml_file, 'r', encoding='utf-8') as file:
                    return yaml.safe_load(file.read())
        except FileNotFoundError as FileNotFound:
            self.logger.error("YAML file: %s does not exist." % (file_path))
            raise FileNotFound
        except TypeError as TyError:
            self.logger.error("The YAML file format is incorrect.")
            raise TyError
        except Exception:
            self.logger.error("File contents are incorrect")

    def jsonFile(self,file_name: Text,file_path=None) -> Dict:
        """
        加载json文件(做特殊兼容处理、自动引入目录：test_data)
        :param file_name: 文件名
        :param file_path: 文件路径
        :return:
        """
        if file_path != None:
            json_file = os.path.join(Route.getPath(file_path),file_name)
        else:
            json_file = os.path.join(Route.getPath("test_data"),file_name)
        try:
            with open(json_file, mode="rb") as data_file:
                json_content = json.load(data_file)
        except json.JSONDecodeError as ex:
            err_msg = "JSONDecodeError:\nfile: %s\nerror: %s"%(file_name,ex)
            raise FileFormatError(err_msg)
        return json_content

    def csvFile(self,file_name: Text,file_path: Text=None) -> List[Dict]:
        """
        加载CSV文件(做特殊兼容处理、自动引入目录：test_data)
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
        if file_path != None:
            csv_file = os.path.join(file_path,file_name)
        else:
            csv_file = os.path.join(Route.getPath("test_data"),file_name)
        csv_content_list = []
        with open(csv_file, encoding="utf-8") as csvfile:
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

Loader = Loader()

if __name__ == '__main__':
    yaml_data = Loader.yamlFile(r"../conf/user_variables/user.yaml")
    json_data = Loader.jsonFile(r"../debug/test_change_type.json")
    csv_data = Loader.csvFile(r"order_sn.csv")
    print("%s\n%s\n%s"%(yaml_data,json_data,csv_data[0]))