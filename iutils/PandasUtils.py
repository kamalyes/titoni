# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
"""
# FileName： PandasUtils.py
# Author : YuYanQing
# Desc: 处理Pandas
# Date： 2021/8/1 1:07
"""
import os
import pandas as pd


class PandasHelper:
    def __init__(self, module_name: str, file_name: str):

        _data_path = os.path.dirname(os.path.dirname(os.path.abspath(
            __file__))) + '/Data/' + module_name

        if file_name.split(".")[-1] == "csv":
            self._csv = pd.read_csv(os.path.join(_data_path, file_name))

        else:
            self._df = pd.read_excel(os.path.join(_data_path, file_name),
                                     na_values=None,
                                     keep_default_na=False)

    def get_excel_data(self):
        """
        用pandas对excel里的数据进行获取
        :return: 返回值格式为列表里包含字典[{},{},{}.....]
        """
        try:
            _data = []
            for _i in self._df.index.values:
                # 用表格里每行遍历出来的值用字典的方式保存在row_data中
                _row_data = self._df.loc[_i].to_dict()
                _data.append(_row_data)
            return _data

        except FileNotFoundError:
            print('读取数据的文件不存在,请检查文件路径！')
            return False

        except Exception as e:
            print('读取数据失败 -> 错误原因 : {}'.format(e))
            return False

    def get_csv_data(self):
        """
        用pandas对csv里的数据进行获取
        :return:
        """
        csv_data = self._csv.values.tolist()
        return csv_data

    def get_excel_param_data(self):
        """
        回去参数化参数列表
        :return: 返回值格式为列表里包含字典[[],[],[].....]
        """
        return self._df.values.tolist()


if __name__ == '__main__':
    test = PandasHelper('variables', 'test.xlsx')
    print(test._df.values.tolist())
    pass
