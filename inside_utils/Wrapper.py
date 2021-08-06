# -*- coding:utf-8 -*-
# Python version 2.7.16 or 3.7.6
'''
# FileName： Wrapper.py
# Author : YuYanQing
# Desc: 语法糖（装饰器模块）
# Date： 2021/7/5 11:37
'''
from inside_utils.LogUtils import Logger
from functools import (wraps, WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES)
logger = Logger.writeLog()

def countTime(model):
    """
    给目标函数加上计算运行时间统计
    """
    # 这个装上器和update_wrapper一样，默认参数WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES
    def init_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            # 定义result接收函数返回值，并且在装饰函数最后返回回去
            resutl = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            if elapsed_time<3:
                logger.info('%s-总耗时：%s(正常范围内)' % (model, elapsed_time))
            elif elapsed_time>5 and elapsed_time<10:
                logger.warning('%s-总耗时：%s(需要注意)' % (model, elapsed_time))
            else:
                logger.error('%s-总耗时：%s(超时)' % (model, elapsed_time))
            return resutl
        # 其中默认参数 WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES
        # update_wrapper(wrapper, func)
        return wrapper
    return init_wrapper

if __name__ == '__main__':
    import time
    @countTime("（自定义模块名）")
    def add(num=100):
        """
        计算 0~num 累加值，默认num=100
        """
        time.sleep(1)
        return sum([x for x in range(num + 1)])

    print('函数名：', add.__name__)
    print('属性字典：', add.__dict__)
    print('函数默认参数：', add.__defaults__)
    print('函数所在模块：', add.__module__)
    print('函数文档：', add.__doc__)
    # 打印两个默认参数
    # WRAPPER_ASSIGNMENTS ：__module__', '__name__', '__qualname__', '__doc__', '__annotations__
    # WRAPPER_UPDATES：__dict__
    print(WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES)
    result = add()
    print(result)