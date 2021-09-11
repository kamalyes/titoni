# -*- coding:utf-8 -*-
# !/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# File  : MySQLUtils.py
# Author: YuYanQing
# Desc  : MySQL驱动类
# Date  : 2020/10/15 9:11
'''
import allure
import pymysql
import pandas as pd

class MysqlTools(object):
    def __init__(self, host, user, pass_word, database=None, port=3306):
        self.MYSQL_HOST = host
        self.MYSQL_USER = user
        self.MYSQL_PW = pass_word
        self.MYSQL_DATABASE = database
        self.MYSQL_PORT = port
        self.conn = None
        self.cur = None

    def init(self):
        """
        连接数据库
        """
        self.conn = pymysql.connect(
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            user=self.MYSQL_USER,
            password=self.MYSQL_PW,
            database=self.MYSQL_DATABASE,
            charset='utf8')
        self.cur = self.conn.cursor()

    def callSql(self, sql):
        '''
        查询数据
        返回结果为pandas的DataFrame
        '''
        try:
            pd_data = pd.read_sql_query(sql, self.conn)
            with allure.step("Database query operation"):
                allure.attach(name="{}".format(sql), body=str(pd_data).strip())
            return pd_data
        except Exception as e:
            raise Exception('sql:%s,error:%s' % (sql, e))

    def doSql(self, sql):
        '''
        修改数据
        执行相关sql
        '''
        try:
            self.cur.execute(sql)
            self.conn.commit()
            with allure.step("Database insert/update operation"):
                allure.attach(name="{}".format(str(sql).split(" ")[0].title()), body=str(sql).strip())
        except Exception as e:
            raise Exception('sql:%s,error:%s' % (sql, e))

    def toSql(self, df, table_name, index=False):
        '''
        DataFrame写入mysql的table
        '''
        df.toSql(table_name, self.conn, index=index)

    def restart(self):
        """
        重启
        """
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        self.init()

    def __del__(self):
        '''
        对象结束
        '''
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

if __name__ == '__main__':
    msq = MysqlTools(host='localhost', user='root', pass_word='1235678', database='test_api', port=3306)
    msq.init()  # init函数为连接数据库
    tables = msq.callSql('show tables')
    print(tables)
    data = msq.callSql("select * from employees")
    print(data)
    msq.restart()