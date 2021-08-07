# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# File  : IDCards.py
# Author: YuYanQing
# Desc  : 身份证效验&随机生成身份证信息
# Date  : 2020/10/15 15:01
'''
import re
import sys
import random
sys.path.append('../')
from inside_utils import AreaCode
from datetime import datetime, timedelta

class IdNumber(str):
    def __init__(self, id_number=None):
        super(IdNumber, self).__init__()
        self.id = id_number
        self.area_id = int(self.id[0:6])
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def getAreaName(self):
        """根据区域编号取出区域名称"""
        return AreaCode.AREA_INFO[self.area_id]

    def getBirthday(self):
        """通过身份证号获取出生日期"""
        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)

    def getAge(self):
        """通过身份证号获取年龄"""
        now = (datetime.now() + timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    def getSex(self):
        """通过身份证号获取性别， 女生：0，男生：1"""
        return int(self.id[16:17]) % 2

    def getCheckDigit(self):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'

    @classmethod
    def checkVerifyId(cls, id_number) ->str:
        """校验身份证是否正确"""
        if re.match(AreaCode.ID_NUMBER_18_REGEX, id_number):
            check_digit = cls(id_number).getCheckDigit()
            return str(check_digit) == id_number[-1]
        else:
            return bool(re.match(AreaCode.ID_NUMBER_15_REGEX, id_number))

    @classmethod
    def getIDCard(cls, sex=0):
        """随机生成身份证号，sex = 0表示女性，sex = 1表示男性"""
        # 随机生成一个区域码(6位数)
        id_number = str(random.choice(list(AreaCode.AREA_INFO.keys())))
        # 限定出生日期范围(8位数)
        start, end = datetime.strptime("1960-01-01", "%Y-%m-%d"), datetime.strptime("2020-12-30", "%Y-%m-%d")
        birth_days = datetime.strftime(start + timedelta(random.randint(0, (end - start).days + 1)), "%Y%m%d")
        id_number += str(birth_days)
        # 顺序码(2位数)
        id_number += str(random.randint(10, 99))
        # 性别码(1位数)
        id_number += str(random.randrange(sex, 10, step=2))
        # 校验码(1位数)
        return id_number + str(cls(id_number).getCheckDigit())


if __name__ == '__main__':
    random_sex = random.randint(0, 1)  # 随机生成男(1)或女(0)
    idcard = IdNumber.getIDCard(random_sex)# 随机生成身份证号
    print(IdNumber(idcard).area_id)  # 地址编码:431121
    print(IdNumber(idcard).getAreaName())  # 地址:湖南省永州市祁阳县
    print(IdNumber(idcard).getBirthday())  # 生日:1999-3-15
    print(IdNumber(idcard).getAge())  # 年龄:21(岁)
    print(IdNumber(idcard).getSex())  # 性别:1(男)
    print(IdNumber(idcard).getCheckDigit())  # 校验码:1
    print(IdNumber.checkVerifyId("411424197912081942"))
