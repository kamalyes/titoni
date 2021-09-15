# -*- coding:utf-8 -*-
# Python version 2.7.16 or 3.7.6
'''
# FileName： Template.py
# Author : YuYanQing
# Desc: 数据替换
# Date： 2021/6/6 0:37
'''
import re
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
                'delim': re.escape(cls.delimiter),
                'id': cls.idpattern,
                'bid': cls.braceidpattern or cls.idpattern,
            }
        cls.pattern = re.compile(pattern, cls.flags | re.VERBOSE)

class Template(metaclass=TemplateMeta):
    """支持$-替换的字符串类"""
    delimiter = '$'
    idpattern = r'(?a:[_a-z][_a-z0-9]*)'
    braceidpattern = None
    flags = re.IGNORECASE

    def __init__(self, template):
        if isinstance(template, dict):
            self.template = str(template)

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(keepends=True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(''.join(lines[:-1]))
            lineno = len(lines)
        error = self.template[int(colno) - 3:len(str(self.template))]
        raise ValueError('Invalid placeholder in string: line %d, col %d\n %s' % (lineno, colno, error))

    def subStitute(self, mapping, disable_data="", genre=None):
        """
        合并数据
        :param mapping: 新的键值对
        :param disable_data:  无需参与类型转化的键值
        :param genre:    转化类型 若不添加则转为Json 若=dict则转为dict类型
        Example::
                >>> general_data = {"name":"${name}","pic":"${pic}"}
                >>> replace_str = {"name": "test0001_name","pic": "test_0001_pic",
                               "randSample":"test_rand_sample","src":"test_0001_src","randLetters":"test_rand_letters"}
                >>> Template(general_data).subStitute(replace_str)
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
            raise ValueError('Unrecognized named group in pattern', self.pattern)
        return eval(
            self.pattern.sub(convert, self.template)) if genre == "dict" and disable_data is "" else conversType(
            eval(self.pattern.sub(convert, self.template)), disable_data)
