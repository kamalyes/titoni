# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# @FileName： JsonUtils.py
# @Author : YuYanQing
# @Desc: 处理Json文件
# @Date： 2021/8/1 11:43 
'''
import os
import json
import difflib

def wirteJson(self, target_data, file_path, method="w"):
    """
    写入Json
    :param target_data:
    :param file_path:
    :param method: 谨慎使用"a"追加模式（可能存在覆盖键值、json格式不对无法提取出来）
    :return:
    """
    method = method if method != "w" else "w"
    if method == "a" and os.path.exists(file_path):
        bak_data = self.readJsonFile(file_path)
        datum = {"old_data": bak_data, "new_data": target_data}
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(datum, file, ensure_ascii=False, indent=4)
    elif method == "w" and os.path.exists(file_path) is False:
        with open(file_path, method, encoding="utf-8") as file:
            json.dump(target_data, file, ensure_ascii=False, indent=4)
    else:
        print("读取Json文件暂只支持w、a模式")

def diffJson(self, filename1, filename2, targetPath):
    """
    比较两个文件内容的md5值；比较两个文件并输出到html文件中
    :param filename1:
    :param filename2:
    :param targetPath:
    :return:
    """
    file1Md5 = self.md5_file(filename1)
    file2Md5 = self.md5_file(filename2)

    if file1Md5 != file2Md5:
        text1_lines = self.read_json(filename1)
        text2_lines = self.read_json(filename2)
        d = difflib.HtmlDiff()
        # context=True时只显示差异的上下文，默认显示5行，由numlines参数控制，context=False显示全文，差异部分颜色高亮，默认为显示全文
        result = d.make_file(
            text1_lines, text2_lines, filename1, filename2, context=True)
        # 内容保存到result.html文件中
        try:
            with open(targetPath, 'a', encoding='utf-8') as result_file:
                result_file.write(result)
        except Exception as e:
            self.logger.error("写入文件失败:" + e)
