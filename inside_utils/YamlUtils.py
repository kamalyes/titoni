# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： ReplaceUtils.py
# Author : YuYanQing
# Desc: 对yaml格式的配置文件的操作
# Date： 2020/7/15 16:15
'''
import sys,yaml
sys.path.append('../')
from inside_utils.Loader import Loader
from inside_utils.LogUtils import Logger
from inside_utils.JsonPath import JsonPath

class YamlHandle(object):
    def __init__(self):
        self.logger = Logger.writeLog()

    def writeOjb(self,file_path, data,method):
        """
        把对象object写入yaml文件
        :param yaml_file: yaml文件地址
        :param obj: 数据对象
        :param method w-->写入新的 a-->追加
        :return:
        """
        with open(file_path, method, encoding='utf-8') as file:
            yaml.dump_all(documents=[data], stream=file, allow_unicode=True, default_flow_style=False, indent=4)

    def getValue(self,file_path, keyword):
        """
        获取yaml里面对应key的value
        :param file_path:
        :param keyword:
        :return:
        """
        data = Loader.yamlFile(file_path)
        try:
            params = JsonPath.find(data,str(keyword))
            self.logger.info('获取配置文件的值，key：{}, data：{}'.format(keyword, params))
        except Exception:
            self.logger.exception('没有获取到对应的值，key：{}, data：{}'.format(keyword, params))
        return params

    def saveData(self,file_path,obj,method=None):
        """
        保存数据 暂不支持复杂类型
        :param obj
        :param method global -->全量 temp--> 临时
        :return:
        """
        old = Loader.yamlFile(file_path)
        if old !=None:
            for k,v in obj.items():
                if k in old:
                    self.logger.error("该变量值已被占用")
                else:
                    self.writeOjb(file_path, obj, method)
        else:
            self.writeOjb(file_path, obj, method)

YamlHandle = YamlHandle()

if __name__ == '__main__':
    import os
    from BaseSetting import Route
    file_path = os.path.join(Route.getPath("user_variables"),"global.yaml")
    YamlHandle.writeOjb(file_path,{"case_info":{"test_list":{"accept":"test"}}},"w")
    YamlHandle.saveData(file_path,{"case_info":"test_list"},"a")
    YamlHandle.getValue(file_path,"$.case_info.test_list")