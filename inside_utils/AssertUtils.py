# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： AssertUtils.py
# Author : YuYanQing
# Desc: 效验结果集
# Date： 2021/3/27 18:05
'''
import re,sys
import allure,operator
sys.path.append('../')
from jsonpath import jsonpath
from inside_utils.LogUtils import Logger

class Assertion:
    def __init__(self):
        self.logger = Logger.writeLog()

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
                        self.check_json(src_data[this_key], dst_data[this_key])
                    elif not isinstance(src_data[this_key], type(dst_data[this_key])):
                        raise Exception("JSON格式校验，关键字 %s 返回结果 %s 与期望结果 %s 类型不符"
                                        % (this_key, src_data[this_key], dst_data[this_key]))
                    else:
                        pass
        else:
            raise Exception("JSON校验内容非dict格式：{}".format(src_data))

    def checkResult(self,case_data, code, data):
        """
        校验测试结果
        :param case_data: 用例数据
        :param code: 接口状态码
        :param data: 返回的接口json数据
        :return:
        """
        try:
            # 获取用例检查信息
            check_type = case_data['response']['check_type']
            expected_code = case_data['response']['expected_code']
            expected_content = case_data['response']['expected_content']
        except Exception as e:
            raise KeyError('获取用例检查信息失败：{}'.format(e))
        # 接口数据校验
        if check_type == 'no_check':
            with allure.step("不校验接口结果"):
                pass
        elif check_type == 'check_code':
            with allure.step("仅校验接口状态码"):
                allure.attach(name="实际code", body=str(code))
                allure.attach(name="期望code", body=str(expected_code))
                allure.attach(name='实际data', body=str(data))
            if int(code) != expected_code:
                raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

        elif check_type == 'check_json':
            with allure.step("JSON格式校验接口"):
                allure.attach(name="实际code", body=str(code))
                allure.attach(name="期望code", body=str(expected_code))
                allure.attach(name='实际data', body=str(data))
                allure.attach(name='期望data', body=str(expected_content))
            if int(code) == expected_code:
                if not data:
                    data = "{}"
                self.check_json(expected_content, data)
            else:
                raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

        elif check_type == 'entirely_check':
            with allure.step("完全校验接口结果"):
                allure.attach(name="实际code", body=str(code))
                allure.attach(name="期望code", body=str(expected_code))
                allure.attach(name='实际data', body=str(data))
                allure.attach(name='期望data', body=str(expected_content))
            if int(code) == expected_code:
                result = operator.eq(expected_content, data)
                if not result:
                    raise Exception("完全校验失败！ %s ! = %s" % (expected_content, data))
            else:
                raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

        elif check_type == 'regular_check':
            if int(code) == expected_code:
                try:
                    result = ""
                    if isinstance(expected_content, list):
                        for i in expected_content:
                            result = re.findall(i.replace("\"", "\""), str(data))
                            allure.attach('校验完成结果\n', str(result))
                    else:
                        result = re.findall(expected_content.replace("\"", "\'"), str(data))
                        with allure.step("正则校验接口结果"):
                            allure.attach(name="实际code", body=str(code))
                            allure.attach(name="期望code", body=str(expected_code))
                            allure.attach(name='实际data', body=str(data))
                            allure.attach(name='期望data', body=str(expected_content).replace("\'", "\""))
                            allure.attach(name=expected_content.replace("\"", "\'") + '校验完成结果',
                                          body=str(result).replace("\'", "\""))
                    if not result:
                        raise Exception("正则未校验到内容！ %s" % expected_content)
                except KeyError:
                    raise Exception("正则校验执行失败！ %s\n正则表达式为空时" % expected_content)
            else:
                raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))
        else:
            raise Exception("无该接口校验方式%s" % check_type)

    def assertNotNull(self,parm):
        """
        验证不为空
        :param parm:
        :return:
        """
        if parm !=None:
            return True

    def assertNotIn(self,parm,list_param):
        """
        验证值不存在
        :param parm:
        :param list_param:
        :return:
        """
        try:
            assert parm not in list_param
            return True
        except Exception:
            self.logger.error('AssertionError: param  {parm} in  list_param  {list_param}  ')
            raise

    def assertIn(self,parm,list_param):
        """
        验证值存在
        :param parm:
        :param list_param:
        :return:
        """
        try:
            assert parm in list_param
            return True
        except Exception:
            self.logger.error('AssertionError: param  {parm} not in  list_param  {list_param}  ')
            raise

    def assertCode(self, code, expect_code):
        """
        验证response中code与预期值一致
        :param code:
        :param expect_code:
        :return:
        """
        try:
            assert code == expect_code
            return True
        except Exception:
            self.logger.error('AssertionError: expect_code is %s, statusCode is %s ' % (expect_code, code))
            raise

    def assertBody(self, body, body_msg, expected_msg):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:
        :param comment:
        :return:
        """
        try:
            msg = body[body_msg]

            assert msg == expected_msg
            return True
        except Exception as e:
            self.logger.error(
                "Response body msg != expected_msg, expected_msg is %s, body_msg is %s" % (expected_msg, body_msg))
            raise

    def assertKv(self, response_msg, expect_msg):
        """
        验证response response_msg中是否包含期望返回值key-value是否相等或key存在
        :param response_msg:
        :param expect_msg:
        :return:
        """

        try:
            if isinstance(expect_msg, dict):
                for key in expect_msg.keys():
                    assert key in response_msg
                    if isinstance(expect_msg[key], list):
                        for i in range(len(expect_msg[key])):
                            self.assert_kv(response_msg[key][i], expect_msg[key][i])
                    elif isinstance(expect_msg[key], dict):
                        self.assert_kv(response_msg[key], expect_msg[key])
                    elif expect_msg[key] != '':
                        assert expect_msg[key] == response_msg[key]
            else:
                assert response_msg == expect_msg

            return True
        except Exception:
            self.logger.error("AssertionError:\n expect_key   is %s \n responseText is %s" % (expect_msg, response_msg))
            raise

    def assertJson(self, response_msg, json_path, expect_data, method):
        """
        对比json内容
        :param response_msg: 返回信息
        :param json_path: json_path
        :param expect_data: 预期
        :param method: in, == 验证
        :return:
        """
        if method == 'in':
            json_path_val = jsonpath(response_msg, json_path)[0]
            try:
                assert expect_data in json_path_val
            except Exception:
                self.logger.error("AssertionError:  %s not in  %s" % (expect_data, json_path_val))
                raise
        elif method == 'equal':
            json_path_val = jsonpath(response_msg, json_path)[0]
            try:
                assert expect_data == json_path_val
            except Exception:
                self.logger.error("AssertionError:  %s not equal  %s" % (expect_data, json_path_val))
                raise
        elif method == 'Unequal':
            json_path_val = jsonpath(response_msg, json_path)[0]
            try:
                assert expect_data != json_path_val
            except Exception:
                self.logger.error("AssertionError:  %s not equal  %s" % (expect_data, json_path_val))
                raise
        elif method == 'length':
            json_path_val = jsonpath(response_msg, json_path)[0]
            try:
                assert expect_data == len(json_path_val)
            except Exception:
                self.logger.error("AssertionError:  %s length is not   %s" % (expect_data, json_path_val))
                raise
        elif method == "<=":
            try:
                assert expect_data <= response_msg
            except Exception:
                self.logger.error("AssertionError:  %s length is not  <=  %s" % (expect_data, response_msg))
                raise
        elif method == "==":
            try:
                assert expect_data <= response_msg
            except Exception:
                self.logger.error("AssertionError:  %s length is not    %s" % (expect_data, response_msg))
                raise
        else:
            raise
