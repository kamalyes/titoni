# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： FolderUtils.py
# Author : YuYanQing
# Desc: 文件管理
# Date： 2020/5/6 19:15
'''
import os
import shutil
import zipfile
from BaseSetting import Route
from iutils.LogUtils import Logger

class FileHander(object):
    def __init__(self):
        self.logger = Logger.writeLog()

    def getCurrentPath(self):
        """
        获取当前文件路径
        :return: pwd
        """
        pwd = os.path.abspath(os.path.dirname(__file__))
        return pwd

    def getSuperiorDir(self):
        """
        获取上级目录
        :return:  superior_directory
        """
        superior_directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        return superior_directory

    def getDirList(self, file_path):
        '''
        获取指定目录下所有的文件名并返回一个列表，剔除其中的__init__.py和__pycache__。
        :param file_path:
        :return:
        '''
        current_files = os.listdir(file_path)
        all_files = []
        for file_name in current_files:
            full_file_name = os.path.join(file_path, file_name)
            all_files.append(full_file_name)
            if os.path.isdir(full_file_name):
                next_level_files = self.getDirList(full_file_name)
                all_files.extend(next_level_files)
        return all_files

    def tarFile(self, method, file_path, target_path=""):
        """
        打包文件为压缩包
        :param file_path  被打包的文件路径
        :param target_path 目标存储的文件路径
        :param method    用于判断是打包单个文件还是遍历文件夹下所有的文件 singfile: 单个、 allfile： 全部
        :param zip_file 声明打包对象、mode改为‘w’
        :param ziplist   多级目录绝对路径
        :return:
        """
        ziplist = []
        zip_file = zipfile.ZipFile(target_path, "w")
        try:
            if not os.path.exists(file_path):
                self.logger.error('请检查file_path是否正确！')
            else:
                if method == "singfile":
                    zip_file.write(file_path)
                if method == "allfile":
                    hasPDir = not file_path.endswith(os.sep);
                    self.logger.info(hasPDir)
                    if not hasPDir:
                        file_path = os.path.dirname(file_path);
                        self.logger.error(file_path)
                    target_path = os.path.dirname(file_path) + os.sep + target_path;
                    self.logger.info("压缩存储后的路径：" + target_path)
                    if not os.path.exists(os.path.dirname(target_path)):
                        os.makedirs(os.path.dirname(target_path));
                    # 多级目录读取
                    for dirpath, dirnames, filenames in os.walk(file_path):
                        for filename in filenames:
                            ziplist.append(os.path.join(dirpath, filename))
                    for tar in ziplist:
                        zip_file.write(tar)
        except Exception as IOError:
            self.logger.error(IOError)
        finally:
            zip_file.close()

    def unZip(self, method, file_path, target_path=""):
        """
        解压多种类型的压缩包
        :param method: 类型判断
        :param file_path: 需要解压的文件绝对路径
        :param zip_list: 获取压缩包内所有的文件
        :return:
        """
        try:
            zip_file = zipfile.ZipFile(file_path)
            if method == "gzip":
                zip_file.extractall(path=target_path)

            if method == "zip":
                zip_list = zip_file.namelist()
                for f in zip_list:
                    zip_file.extract(f, target_path)
            else:
                pass
        except Exception as IOError:
            self.logger.error(IOError)

        finally:
            zip_file.close()

    def getFileState(self, file_path):
        """
        判断传入的文件状态
        :param file_path:  检查的文件路径
        备注：实际用os自带的即可
        """
        try:
            if os.access(file_path, os.F_OK):
                self.logger.info("%s：文件存在" % (file_path))
                if os.access(file_path, os.R_OK):
                    self.logger.info("%s：文件可读" % (file_path))
                else:
                    self.logger.error("%s：文件不支持可读" % (file_path))

                if os.access(file_path, os.W_OK):
                    self.logger.info("%s：文件可写" % (file_path))
                else:
                    self.logger.error("%s：文件不支持可写" % (file_path))

                if os.access(file_path, os.X_OK):
                    self.logger.info("%s：文件可执行" % (file_path))
                else:
                    self.logger.error("%s：文件不支持可执行" % (file_path))

                if (os.path.isdir(file_path)):
                    self.logger.info("%s：这是一个文件夹" % (file_path))
                else:
                    self.logger.info("%s：这是一个文件" % (file_path))
            else:
                self.logger.error("%s：文件不存在" % (file_path))
        except Exception as IOError:
            self.logger.error(IOError)

    def copyFile(self, file_path, target):
        """
        复制文件
        :param method:
        :param file_path:
        :param target:
        :return:
       """
        file_list = []
        if os.path.exists(file_path):
            if not os.path.exists(target):
                os.makedirs(target)
            # 多级目录读取
            for dirpath, dirnames, filenames in os.walk(file_path):
                for filename in filenames:
                    file_list.append(os.path.join(dirpath, filename))
            for list in file_list:
                shutil.copy(list, target)
        else:
            self.logger.error('请检查file_path是否正确！')
        return target

    def removeFile(self, file_path):
        """
        删除文件或文件夹
        :param file_path:
        :return:
        """
        try:
            if os.path.exists(file_path):
                for root, dirs, files in os.walk(file_path, topdown=False):
                    # 先删除文件
                    for name in files:
                        os.remove(os.path.join(root, name))
                    # 再删除空目录
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                        # 再删除自己
                        os.rmdir(file_path)
            else:
                self.logger.error('请检查file_path是否正确！')
        except Exception as FileNotFoundError:
            self.logger.error(FileNotFoundError)

    def makeFile(self, file_path):
        """
        递归创建多级文件夹
        :param file_path:
        :return:
        """
        try:
            if not os.path.exists(file_path):
                os.makedirs(file_path, exist_ok=True)
                if os.path.exists(file_path):
                    self.logger.info("目录：%s 创建成功！！！" % (file_path))
            else:
                self.logger.error("%s已存在，跳过创建！" % (file_path))
        except Exception as FileNotFoundError:
            self.logger.error(FileNotFoundError)

    def depthScanFile(self, catalog, file_type):
        """
        过滤xxx目录下所有的xx格式文件
        :param catalog: 指定目录
        :param file_type 类型
        :return:
        """
        file_list = os.listdir(catalog)
        yaml_files = []
        for index in range(len(file_list)):
            name, suffix = os.path.splitext(file_list[index])
            # 判断文件类型
            if suffix.replace(".", "").lower() == file_type:
                yaml_files.append("%s\\%s" % (catalog, file_list[index]))
        return yaml_files

    def readFileType(self, file_path):
        """
        获取文件类型
        :param file_path:
        :return:
        """
        if file_path is None or os.path.isfile(file_path) == False:
            raise "Please check whether the file path or file name exists"
        else:
            head, tail = os.path.split(file_path)
            name, suffix = os.path.splitext(tail)
            return suffix.lower()

FileHander = FileHander()

if __name__ == '__main__':
    # file_path =r"..\result"
    # FileHander.tarFile(method="allfile",file_path=file_path,target_path="tarFile.gzip")
    # FileHander.getFileState(file_path)
    # FileHander.copyFile(file_path,file_path)
    # FileHander.removeFile(file_path)
    # FileHander.makeFile(file_path)
    # FileHander.getDirList(file_path)
    print(FileHander.depthScanFile(Route.getPath("variables"), "yaml"))
    print(FileHander.readFileType(os.path.join(Route.getPath("variables"), "global.yaml")))
