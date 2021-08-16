# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： DateUtils.py
# Author : YuYanQing
# Desc: 日期处理类库
# Date： 2020/9/17 19:05
'''
import time
import datetime

class Moment(object):
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

    def computeDate(self, days=0,seconds=0, microseconds=0,
                milliseconds=0, minutes=0, hours=0, weeks=0,custom=None):
        """
        日期偏移
        :param days:
        :param seconds:
        :param microseconds:
        :param milliseconds:
        :param minutes:
        :param hours:
        :param weeks:
        :param custom：自定义
        :return:
        """
        if custom is not None:
            today = datetime.datetime.strptime(custom,'%Y-%m-%d %H:%M:%S')
        else:
            today = datetime.datetime.now()
        return (today + datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)).strftime('%Y-%m-%d %H:%M:%S')

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

    def setSleepTime(self,timestamp):
        """
        休眠xx时间
        :param timestamp:
        :return:
        """
        time.sleep(timestamp)

    def compareTime(self,time1,time2):
        """
        时间比较
        :param time1:
        :param time2:
        :return:
        """
        time1 = datetime.datetime.strptime(time1,'%Y-%m-%d %H:%M:%S')
        time2 = datetime.datetime.strptime(time2,'%Y-%m-%d %H:%M:%S')
        if time1>time2:
            return True
        else:
            return False

Moment = Moment()

if __name__ == "__main__":
    print(Moment.getTime("%Y-%m-%d %H:%M:%S"))
    print(Moment.getTime("10timestamp"))
    print(Moment.getTime("13timestamp"))
    print(Moment.computeDate(-6))
    print(Moment.timestampToDate(1603282677.5209892))
    print(Moment.getEveryDay("2020-06-05", "2020-07-01"))
    print(Moment.getSingletime("2020-06-01 18:50:00"))
    print(Moment.compareTime("2021-08-23 17:11:37", "2021-08-22 17:11:37"))