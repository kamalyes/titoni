# -*- coding:utf-8 -*-
# Python version 2.7.16 or 3.7.6
'''
# FileName： Template.py
# Author : YuYanQing
# Desc: 数据替换
# Date： 2021/6/6 0:37
'''
import re
import sys
from BaseSetting import Route
sys.path.append('../')
from iutils.Loader import Loader
from iutils.DataKit import conversType

class TemplateMeta(type):
    pattern = r"""
    %(delim)s(?:
      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters
      (?P<named>%(id)s)      |   # delimiter and a Python identifier
      {(?P<braced>%(bid)s)}  |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    """
    def __init__(cls, name, bases, dct):
        super(TemplateMeta, cls).__init__(name, bases, dct)
        if 'pattern' in dct:
            pattern = cls.pattern
        else:
            pattern = TemplateMeta.pattern % {
                'delim' : re.escape(cls.delimiter),
                'id'    : cls.idpattern,
                'bid'   : cls.braceidpattern or cls.idpattern,
                }
        cls.pattern = re.compile(pattern, cls.flags | re.VERBOSE)

class Template(metaclass=TemplateMeta):
    """支持$-替换的字符串类"""
    delimiter = '$'
    idpattern = r'(?a:[_a-z][_a-z0-9]*)'
    braceidpattern = None
    flags = re.IGNORECASE

    def __init__(self, template):
        if isinstance(template,dict):
            self.template = str(template)

    def subStitute(self,mapping,disable_data="",type=None):
        """
        合并数据
        :param mapping: 新的键值对
        :param disable_data:  无需参与类型转化的键值
        :param type:    转化类型 若不添加则转为Json 若=dict则转为dict类型
        :return:
        """
        def convert(mo):
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                return str(mapping[named])
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern',self.pattern)
        return eval(self.pattern.sub(convert, self.template)) if type =="dict" and disable_data is "" else conversType(eval(self.pattern.sub(convert, self.template)),disable_data)

if __name__ == '__main__':
    general_data = Loader.jsonFile(Route.joinPath("test_json","create_virtual_product.json"))
    replace_str = {'category_id': 15888, 'name': '自动化_虚拟商品7eN95a',
                   'pic': 'http://file.vetscloud.com/2008e57c7feb8135f2754ba939a1bb41,http://file.vetscloud.com/830beab89f997daf4ff62d9c50dc98c5,http://file.vetscloud.com/3e62fed5130d6a9f8dd196b4719f4a6e,http://file.vetscloud.com/9db24b0c2c4a9d2edce96cabadc1a521,http://file.vetscloud.com/d55dc27a512ede0547e99d9fdb894e18',
                   'selling_point': '', 'term_value': '2021-07-21 13:34:33', 'market_price': 157, 'retail_price': 157,
                   'center_pic': 'http://file.vetscloud.com/0c97a173a6c78848a8fc554f7a65eab6'}
    print(Template(general_data).subStitute(replace_str,["category_id","market_price"]))
