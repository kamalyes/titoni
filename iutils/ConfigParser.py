# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： ConfigParser.py
# Author : YuYanQing
# Desc: ini配置文件处理
# Date： 2021/8/1 21:20
'''

import configparser
from iutils.LogUtils import Logger
logger = Logger.write_log()#调用日志模块

class IniHandle():
    def __init__(self,filepath=None):
        try:
            self.conf = configparser.ConfigParser()
            self.conf.read(filepath, encoding="utf-8")
        except Exception as FileNotFoundError:
            logger.error("文件读取失败，请检查%s是否存在,错误信息：%s" % (filepath,FileNotFoundError))

    @classmethod
    def openConfig(self,filepath=None):
        """
        打开指定的ini文件
        :param filepath:
        :return: <configparser.ConfigParser object at 0x0000015940785BA8>
        """
        try:
            conf = configparser.ConfigParser()
            conf.read(filepath, encoding="utf-8")
            return conf
        except Exception as FileNotFoundError:
            logger.error("文件读取失败，请检查%s是否存在,错误信息：%s"%(filepath,FileNotFoundError))

    def checkSection(self, section,option=None):
        """
        检查节点
        :param section:
        :return:
        """
        try:
            if option is None:
                self.conf.has_section(section)
            else:
                self.conf.has_option(section, option)
        except Exception as  e:
            logger.info("无此节点，错误信息%s"%(e))

    def allSection(self):
        """
        获取ini文件下所有的section值
        :return:  all_section
        """
        return self.conf.sections()

    def options(self,section):
        """
        获取指定section的所有option的Key
        :return:
        """
        if self.conf.has_section(section):
            return self.conf.options(section)
        else:
            raise ValueError(section)

    def sectOption(self,section):
        """
        获取指定section下的option的键值对
        :return: List形式的 [('a', 'b'),('aa', 'bb')]
        """
        if self.conf.has_section(section):
            return self.conf.items(section)

    def optValue(self,node,key):
        """
        获取指定section下option的value值
        :param filepath 需要读取的文件
        :param node 父类节点
        :param key  所需要查询内容的单一key
        :return: result 返回对应key的value值
        """
        return self.conf.get(node, key)

    def allItems(self):
        """
        打印配置文件所有的值(该方法并不是很常用)
        :return:
        """
        for section in self.allSection():
            logger.info("[" + section + "]")
            for K, V in self.conf.items(section):
                logger.info(K + "=" + V)

    def readSections(self):
        """
        读取所有section到字典中
        :return:
        """
        res_1 = {}
        res_2 = {}
        sections = self.conf.sections()
        for sec in sections:
            for key, val in self.conf.items(sec):
                res_2[key] = val
            res_1[sec] = res_2.copy()
            res_2.clear()
        return res_1

    def rmseOption(self, section, key=None):
        """
        删除一个 section中的一个item（以键值KEY为标识）
        :param section:
        :param key:
        :return:
        """
        if key is None:
            self.checkSection(section)
            self.conf.remove_section(section)
        else:
            self.checkSection(section, key)
            self.conf.remove_option(section, key)

    def addSection(self, section):
        """
        添加一个section
        :param section:
        :return:
        """
        self.conf.add_section(section)

    def addItem(self, section, key, value):
        """
        往section添加key和value
        :param section:
        :param key:
        :param value:
        :return:
        """
        self.conf.set(section, key, value)

    def readConfig(self):
        conf_ini = r"../Config/config.ini"
        conf = configparser.ConfigParser()
        conf.read(conf_ini, encoding="utf-8")
        return conf

IniHandle = IniHandle()

if __name__ == '__main__':
    filepath = r'../config/config.ini'
    logger.info(IniHandle(filepath))
    IniHandle = IniHandle()
    logger.info(IniHandle.allSection())
    logger.info(IniHandle.openConfig(filepath))
    logger.info(IniHandle.optValue(node="Proxy_Setting",key="proxy_switch"))
    # logger.info(IniHandle().allSection())
    logger.info(IniHandle.options("Proxy_Setting"))
    logger.info(IniHandle.sectOption('Proxy_Setting'))
    # logger.info(IniHandle().allItems())式展示：%s"%(dics))
    IniHandle.checkSection("Proxy_Setting")
    IniHandle.rmseOption(section="rose")
