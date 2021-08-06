# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： DateUtils.py
# Author : YuYanQing
# Desc: 时间获取类
# Date： 2020/9/17 19:05
'''
import time,datetime

class TimeUtil(object):
    def getTime(self,layout)->str:
        """
        获取时间
        :param time_type: 现在的时间now， 其他时间else_time
        :param layout: 10timestamp， 13timestamp,  else  时间类型
        :return:
        """
        tim = datetime.datetime.now()
        temp = tim.strftime('%Y-%m-%d %H:%M:%S')
        # 获取10位时间戳
        if layout == "10timestamp":
            tim = int(time.mktime(time.strptime(temp, "%Y-%m-%d %H:%M:%S")))
        # 获取13位时间戳
        elif layout == "13timestamp":
            datetime_object = datetime.datetime.now()
            now_timetuple = datetime_object.timetuple()
            now_second = time.mktime(now_timetuple)
            tim = now_second*1000 + datetime_object.microsecond/1000
        # 按传入格式获取时间
        else:
            tim = tim.strftime(layout)
        return tim

    def computeDate(self, day_interval):
        """
        日期偏移
        :param day_interval: 想要偏移的天数
        :return
        """
        today = datetime.date.today()
        if isinstance(day_interval, int) and day_interval >= 0:
            return today + datetime.timedelta(days=day_interval)
        elif isinstance(day_interval, int) and day_interval < 0:
            return today - datetime.timedelta(days=abs(day_interval))

    def timestampToDate(self, timestamp):
        """
        时间戳格式化为xxx年xx月xx日
        :return timestamp_to_date
        :param
        :return:
        """
        if not isinstance(timestamp, (int, float)):
            return None
        time_tuple = time.localtime(timestamp)
        specific_data = str(time_tuple[0]) + "-" + str(time_tuple[1]) + "-" + str(time_tuple[2]) + " " \
                        + str(time_tuple[3]) + ":" + str(time_tuple[4]) + ":" + str(time_tuple[5])
        return specific_data

    def getEveryDay(self, start, end):
        """
        中间时差计算
        :param start: 开始日期
        :param end:   结束日期
        :return
        """
        date_list = []
        begin_date = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        print('中间共计%s天' %str(len(date_list)))
        return date_list

    def getSingletime(self, singletime):
        """
        单个日期初始化时间戳年月日时分秒、转化为时间戳
        :param singletime:
        :return
        """
        singletime = time.strptime(singletime, '%Y-%m-%d %H:%M:%S')
        time_stamp = int(time.mktime(singletime))
        return time_stamp

if __name__ == "__main__":
    TimeUtil = TimeUtil()
    print(TimeUtil.getTime("%Y-%m-%d %H:%M:%S"))
    print(TimeUtil.getTime("10timestamp"))
    print(TimeUtil.getTime("13timestamp"))
    print(TimeUtil.computeDate(10))
    print(TimeUtil.computeDate(-6))
    print(TimeUtil.timestampToDate(1603282677.5209892))
    print(TimeUtil.getEveryDay("2020-06-05", "2020-07-01"))
    print(TimeUtil.getSingletime("2020-06-01 18:50:00"))
