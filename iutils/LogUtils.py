# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： LogUtils.py
# Author : YuYanQing
# Desc: 日志处理
# Date： 2020/7/15 16:15
'''
import os
import time,logging,shutil
import datetime,BaseSetting

class Logger(object):
    def __init__(self):
        """
        初始化目录
        :param result_dir 主程序目录
        :param local_data 时间格式存储目录
        :param general_dir
        """
        self.result_dir = BaseSetting.Route.getPath("output")
        self.local_date = time.strftime('%Y-%m-%d-logs', time.localtime(time.time()))
        self.general_dir = os.path.join(self.result_dir,self.local_date)

    def writeLog(self):
        """
        日志处理(写入文本、控制台输出)
        :return:
        """
        if not os.path.exists(self.general_dir):
            os.makedirs(self.general_dir)

        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # 创建defaul_log_handler写入所有日志
        defaul_log = logging.FileHandler(os.path.join(self.general_dir,"%s-default.log"%(self.local_date)),encoding='utf-8')
        defaul_log.setLevel(logging.DEBUG)

        # 创建error_log_handler写入所有日志
        error_log = logging.FileHandler(os.path.join(self.general_dir,"%s-error.log"%(self.local_date)),encoding='utf-8')
        error_log.setLevel(logging.ERROR)

        # 创建console_handler写入所有日志
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        # 定义default日志输出格式 以时间-日志器名称-日志级别-日志内容的形式展示
        all_log_formatter = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s")
        # 定义error日志输出格式  以时间-日志器名称-日志级别-文件名-函数行号-错误内容
        error_log_formatter = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s: %(message)s")
        # 将定义好的输出形式添加到handler
        defaul_log.setFormatter(all_log_formatter)
        console.setFormatter(all_log_formatter)
        error_log.setFormatter(error_log_formatter)

        # 提示：这里需要进行判断如果logger.handlers列表为空，则添加，否则直接去写日志 处理重复打印事件
        if not logger.handlers:
            logger.addHandler(defaul_log)
            logger.addHandler(error_log)
            logger.addHandler(console)
        return logger

    def deleteLog(self, days=None):
        """
        大于多少天的日志自动删除
        :param re_date_unix    前xxx天时间转换为时间戳
        :param days: 偏移量 若为正则往后日期 负值则前多少日
        :return:
        """
        re_date = (datetime.datetime.now() + datetime.timedelta(days=days))
        re_date_unix = int(time.mktime(re_date.timetuple()))
        index = 0
        for dirpath, dirnames, filenames in os.walk(self.result_dir):
            timeArray = os.stat(dirpath).st_mtime
            if timeArray < re_date_unix:
                if index!=0:
                    # print("过期的文件：%s" % (dirpath))
                    shutil.rmtree(dirpath, ignore_errors=True)
            # else:
                # print("不满足条件的文件：%s" % (dirpath))
            index +=1

Logger = Logger()

if __name__ == '__main__':
    logger = Logger.writeLog()
    logger.info("这是Info信息")
    logger.error("这是error信息")
    logger.warning("这是warning信息")