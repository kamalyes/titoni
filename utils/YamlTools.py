# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： YamlTools.py
# Author : YuYanQing
# Desc: YAML文件轻量处理工具类
# Date： 2021/3/26 13:31
'''
import os,yaml

class YamlHander(object):
    def depthScanYaml(self,catalog):
        """
        扫描指定目录下所有的yaml文件
        :param catalog: 指定目录
        :return:
        """
        abs_path = os.path.abspath(catalog)
        file_list = os.listdir(catalog)
        yaml_files = []
        for file in range(len(file_list)):
            head,tail =os.path.splitext(file_list[file])
            if tail ==".yaml" or tail =="YAML":
                yaml_files.append(abs_path+"\\"+file_list[file])
        return yaml_files

    def loadYaml(self,file_path):
        """
        读取Yaml文件
        :param file_path Yaml文件路径
        :return:
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = yaml.safe_load(file.read())
            return content

    def summaryData(self,catalog=None,model=None,file_path=None):
        """
        汇总yaml中的数据转化为case
        :param catalog: 文件目录
        :param model: 模式 若为single则单例只解析一个yml 若不设置则读取文件夹下获取的yaml
        :param file_path: 单个文件地址
        :return:
        """
        yaml_dict = {}
        if model =="single":
            head, tail = os.path.split(file_path)
            case = {tail.replace(".yaml", ""): self.loadYaml(file_path)}
            yaml_dict.update(case)
        elif catalog !=None:
            files = self.depthScanYaml(catalog)
            for i in range(len(files)):
                head,tail = os.path.split(files[i])
                case = {tail.replace(".yaml",""):self.loadYaml(files[i])}
                yaml_dict.update(case)
        else:
            raise Exception("仅支持单例及批量转换！！！")
        return yaml_dict

if __name__ == '__main__':
    YamlHander = YamlHander()
    file_path = r"D:\Work_Spaces\PyCharm_Project\YamlInterfaceTest\Files\registerV2_succeed.har"
    print(YamlHander.summaryData(model = "single",file_path=file_path))
    print(YamlHander.summaryData("../yamldata"))