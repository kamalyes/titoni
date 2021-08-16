# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： SendMsg.py
# Author : YuYanQing
# Desc: 测试报告消息推送
# Date： 2021/8/27 20:05
'''
import math
from iutils.Loader import Loader
from iutils.EmaliUtils import Email
from iutils.JenkinsUtils import Jenkins
from iutils.WxRobotTools import WechatRobot
from testings.control.path import APPPROPERTIES_PATH

SUMMARY = Loader.yamlFile("summary.yaml")
PUSH_CONFIG = Loader.yamlFile("./config/push_message.yaml")
RUN_PATH = Loader.yamlFile(APPPROPERTIES_PATH)["profiles"]
USER = PUSH_CONFIG["jenkins"]["user"]
PASSWORD = PUSH_CONFIG["jenkins"]["password"]
JOB_NAME = PUSH_CONFIG["jenkins"]["job_name"]
BUILD_URL = PUSH_CONFIG["jenkins"]["build_url"]
EMAIL_USER = PUSH_CONFIG["email"]["user"]
EMAIL_PWD = PUSH_CONFIG["email"]["password"]
EMAIL_HOST = PUSH_CONFIG["email"]["host"]
EMAIL_TITLE = PUSH_CONFIG["email"]["title"]
EMAIL_ADDRESS = PUSH_CONFIG["email"]["addressees"]
QYWX_KEY = PUSH_CONFIG["robot"]["debug_qywx_key"]
PRODUCT = PUSH_CONFIG["other"]["product"]
robot_msg = WechatRobot(QYWX_KEY)
duration = "%.2fs"%(SUMMARY["duration"])
count = SUMMARY["total"]
SUCCESS_REOT = math.ceil(SUMMARY["successful"])
passed = SUMMARY["passed"]
failed = SUMMARY["failed"]
skipped = SUMMARY["skipped"]
jenkins = Jenkins(url=BUILD_URL, username=USER, password=PASSWORD)
# fix builds_number未获取到正在进行中的构建
running_builds = jenkins.getRunningBuilds()
if running_builds !=[]:
    for index in running_builds:
        if JOB_NAME in index["name"]:
            LAST_BUILD_NAM = index["number"]
else:
    LAST_BUILD_NAM = jenkins.getJobInfo(JOB_NAME)['lastCompletedBuild']['number']
robot_msg.send_markdown("# **提醒！{}**<font color=\"warning\">**{}环境**</font>\n".format(PRODUCT,RUN_PATH) +  # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                        "#### **请相关同事注意，及时跟进！**\n" +  # 加粗：**需要加粗的字**
                        "> 类型：<font color=\"info\">API自动化</font> \n" +  # 引用：> 需要引用的文字
                        "> 执行总耗时：<font color=\"warning\">{}s</font>\n".format(duration) +
                        "> 用例总数：<font color=\"warning\">{}例</font> \n".format(count) +  # 字体颜色(只支持3种内置颜色)
                        "> 成功率：<font color=\"warning\">{}%</font>\n".format(
                            SUCCESS_REOT) + # 绿色：info、灰色：comment、橙红：warning
                        "> 成功数：<font color=\"info\">{}例</font>\n".format(passed) +
                        "> 失败数：<font color=\"warning\">{}例</font>\n".format(failed) +
                        "> 跳过数：<font color=\"comment\">{}例</font>\n".format(skipped) +
                        "[点击查看Jenkins构建日志]({}/job/{}/{}/console)\n".format(BUILD_URL,JOB_NAME,LAST_BUILD_NAM) +
                        "[点击查看Allure测试报告详情]({}/job/{}/{}/allure)".format(BUILD_URL,JOB_NAME,LAST_BUILD_NAM))
body = """
<!doctype html>
        <html lang="en">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
                <meta charset="utf-8">
                <style>
        .heading {
            margin: 10px;
        }
        .heading .attribute {
            margin-top: 1ex;
            margin-bottom: 0;
        }
                </style>
            </head>
            <body>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-4">
                        <div class='heading'>
                            <div>
                                <p class='attribute'><strong>用例总数：</strong> report_detail_count</p>
                                <p class='attribute'><strong>执行耗时：</strong> report_summary_duration</p>
                                <p class='attribute'><strong>成功率：</strong> SUCCESS_REOT</p>
                                <p class='attribute'><strong>状态：</strong>
                                    <span class="badge badge-success" style="background-color: rgb(0 255 127);">&nbsp;通过：report_summary_status_pass</span>
                                    <span class="badge badge-danger" style="background-color: rgb(255, 99, 132);">&nbsp;失败：report_summary_status_fail&nbsp;</span>
                                    <span class="badge badge-secondary" style="background-color: rgb(201, 203, 207);">&nbsp;跳过：report_summary_status_skip </span>
                                </p>
                                <p class='attribute'><strong>构建日志：</strong> <a href="BUILD_URL/job/JOB_NAME/LAST_BUILD_NAM/console">BUILD_URL/job/JOB_NAME/LAST_BUILD_NAM/console</a></p>
                                <p class='attribute'><strong>Allure报告：</strong> <a href="BUILD_URL/job/JOB_NAME/LAST_BUILD_NAM/allure">BUILD_URL/job/JOB_NAME/LAST_BUILD_NAM/allure</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </body>
        </html>"""
mail_body = str(body).replace("report_detail_count", str(count)) \
    .replace("report_summary_duration", str(duration)) \
    .replace("report_summary_status_pass", str(passed)) \
    .replace("report_summary_status_fail", str(failed)) \
    .replace("report_summary_status_skip", str(skipped)) \
    .replace("SUCCESS_REOT", str(SUCCESS_REOT)) \
    .replace("BUILD_URL", str(BUILD_URL)) \
    .replace("LAST_BUILD_NAM", str(LAST_BUILD_NAM))\
    .replace("JOB_NAME",str(JOB_NAME))
Email = Email(user_email=EMAIL_USER, passwd=EMAIL_PWD, title="({})".format(RUN_PATH)+EMAIL_TITLE,smtp_server=EMAIL_HOST,addressee=EMAIL_ADDRESS)
Email.send(subject='自动执行发送-请勿回复 ', content=mail_body, send_type='html')
