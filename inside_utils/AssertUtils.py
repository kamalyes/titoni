# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AssertUtils.py
# Author : YuYanQing
# Desc: 效验结果集
# Date： 2021/3/27 18:05
'''

import sys
import allure
import operator
sys.path.append('../')

class Assertion:

    def checkJson(self,src_data, dst_data):
        """
        校验的json
        :param src_data: 检验内容
        :param dst_data: 接口返回的数据
        :return:
        """
        if isinstance(src_data, dict):
            for key in src_data:
                if key not in dst_data:
                    raise Exception("JSON格式校验，关键字 %s 不在返回结果 %s 中！" % (key, dst_data))
                else:
                    this_key = key
                    if isinstance(src_data[this_key], dict) and isinstance(dst_data[this_key], dict):
                        self.checkJson(src_data[this_key], dst_data[this_key])
                    elif not isinstance(src_data[this_key], type(dst_data[this_key])):
                        raise Exception("JSON格式校验，关键字 %s 返回结果 %s 与期望结果 %s 类型不符"
                                        % (this_key, src_data[this_key], dst_data[this_key]))
                    else:
                        pass
        else:
            raise Exception("JSON校验内容非dict格式：{}".format(src_data))

    def checkResult(self,check_type,case_data, code, content,text,time,variables):
        """
        校验测试结果
        :param check_type:
        :param variables: 部分字段效验
        :param time: 响应时间
        :param text: 文本值
        :param content: 返回的接口json数据
        :param case_data: 用例数据
        :param code: 接口状态码
        :return:
        """
        try:
            # 获取用例检查信息
            check_type = case_data['response']['check_type']
            expected_code = case_data['response']['expected_code']
            expected_content = case_data['response']['expected_content']
            expected_text = case_data['response']['expected_text']
            expected_time = case_data['response']['expected_time']
            expected_variables = case_data['response']['expected_variables']
        except Exception as e:
            pass
        # 接口数据校验
        if check_type == 'null':
            with allure.step("不校验接口结果"):
                pass
        elif check_type == 'code':
            with allure.step("仅校验接口状态码"):
                allure.attach(name="实际code", body=str(code))
                allure.attach(name="期望code", body=str(expected_code))
            if int(code) != expected_code:
                raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

        elif check_type == 'diff':
            with allure.step("校验接口状态码+Json"):
                allure.attach(name="实际code", body=str(code))
                allure.attach(name="期望code", body=str(expected_code))
                allure.attach(name='实际data', body=str(content))
                allure.attach(name='期望data', body=str(expected_content))
            if int(code) == expected_code:
                result = operator.eq(expected_content, content)
                if not result:
                    raise Exception("完全校验失败！ %s ! = %s" % (expected_content, content))
            else:
                raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

        elif check_type == 'regular':
            with allure.step("正则校验接口结果"):
                allure.attach(name="实际code", body=str(code))
                allure.attach(name="期望code", body=str(expected_code))
                allure.attach(name='实际data', body=str(content))
                allure.attach(name='期望data', body=str(expected_content))
                allure.attach(name='实际text', body=str(text))
                allure.attach(name='期望text', body=str(expected_text))
                allure.attach(name='实际响应time', body=str(time))
                allure.attach(name='期望响应time', body=str(expected_time))
                allure.attach(name='实际variables', body=str(variables))
                allure.attach(name='期望variables', body=str(expected_variables))
            pass