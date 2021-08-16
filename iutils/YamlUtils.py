# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： ReplaceUtils.py
# Author : YuYanQing
# Desc: 对yaml格式的配置文件的操作
# Date： 2020/7/15 16:15
'''
import yaml
import shutil
from iutils.Loader import Loader
from iutils.LogUtils import Logger
from iutils.Processor import JsonPath

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

    def saveData(self,file_path,obj,safe_control=None):
        """
        保存数据 暂不支持复杂类型
        :param obj
        :param safe_control 安全模式 默认启用状态
        :return:
        """
        old_data = Loader.yamlFile(file_path)
        if old_data is None:
            self.writeOjb(file_path, obj, "w")
        else:
            for key,value in obj.items():
                if key in old_data.keys() and safe_control is False:
                    bak_filepath = file_path+".bak"
                    self.logger.warning("键值：%s已存在，生成备份数据：%s"%(key,bak_filepath.split("\\")[-1]))
                    shutil.copy(file_path, bak_filepath)
                    old_data.update(obj)
                    self.writeOjb(file_path, old_data, "w")
                else:
                    self.writeOjb(file_path,obj,"a")

YamlHandle = YamlHandle()

if __name__ == '__main__':
    import os
    from BaseSetting import Route
    file_path = os.path.join(Route.getPath("variables"),"global.yaml")
    YamlHandle.writeOjb(file_path,{"case_info":{"test_list":{"accept":"old_data"}}},"w")
    YamlHandle.saveData(file_path,{"case_info":"test_list"},False)
    YamlHandle.getValue(file_path,"$.case_info.test_list")