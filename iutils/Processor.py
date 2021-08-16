# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： Processor.py
# Author : YuYanQing
# Desc: An XPath for JSON 后置处理
# Date： 2021/6/27 11:50
'''
import re
import sys
from lxml import etree
from typing import Dict, Text
from urllib.parse import unquote
# For python3 portability
if sys.version_info[0] == 3:
    xrange = range

class HtmlPath(object):
    def find(self,res, xpath, index)->Text:
        """
        获取html中的数据
        :param res:
        :param xpath:
        :param index:
        :return:
        """
        return etree.HTML(res).xpath(xpath)[index]

    def border(self, sum_str, left_str, right_str, offset=0):
        """
        根据字符串左右边界获取内容
        offset:要获得匹配的第几个数据,默认第一个
        :param sum_str:
        :param left_str:
        :param right_str:
        :param offset:
        :return:
        """
        regex = '([\\s\\S]*?)'
        r = re.compile(left_str + regex + right_str)
        result = r.findall(sum_str)
        if str(offset) == 'all':
            return result
        else:
            if len(result) >= offset and len(result) != 0:
                return result[offset]
            else:
                return None

class JsonPath():
    def jsonToXwwwForm(self, post_data)->Text:
        """
        将origin dict转换为x-www-form-urlencoded
        Args:
            post_data (dict):{"a": 1, "b":2}
        Returns:
            str:a=1&b=2
        """
        if isinstance(post_data, dict):
            return "&".join(["{}={}".format(key, value) for key, value in post_data.items()])
        else:
            return post_data

    def xwwwFormToJson(self, post_data)->Dict:
        """
        将x-www-form-urlencoded转换为origin dict
        Args:
            post_data (str): a=1&b=2
        Returns:
            dict: {"a":1, "b":2}
        """
        if isinstance(post_data, str):
            converted_dict = {}
            for k_v in post_data.split("&"):
                try:
                    key, value = k_v.split("=")
                except ValueError:
                    raise Exception("Invalid x_www_form_urlencoded data format: {}".format(post_data))
                converted_dict[key] = unquote(value)
            return converted_dict
        else:
            return post_data

    def listToJson(self, origin_list)->Dict:
        """
        将list数据转化为json
        Args:
            origin_list (list)[{"name": "v", "value": "1"}, {"name": "w", "value": "2"}]
        Returns:
            dict:{"v": "1", "w": "2"}
        """
        return {item["name"]: item.get("value") for item in origin_list}

    def normalize(self,filter):
        """
        normalize the path expression; outside jsonpath to allow testings
        :param filter: 需要查找的值
        :return:
        """
        subx = []

        # replace index/filter expressions with placeholders
        # Python anonymous functions (lambdas) are cryptic, hard to debug
        def f1(m):
            n = len(subx)  # before append
            g1 = m.group(1)
            subx.append(g1)
            ret = "[#%d]" % n
            # print("f1:", g1, ret)
            return ret

        filter = re.sub(r"[\['](\??\(.*?\))[\]']", f1, filter)
        filter = re.sub(r"'?(?<!@)\.'?|\['?", ";", filter)
        filter = re.sub(r";;;|;;", ";..;", filter)
        filter = re.sub(r";$|'?\]|'$", "", filter)

        # put expressions back
        def f2(m):
            g1 = m.group(1)
            #       print("f2:", g1)
            return subx[int(g1)]

        filter = re.sub(r"#([0-9]+)", f2, filter)
        return filter

    def find(self,obj, expr, result_type='VALUE', debug=0, use_eval=True):
        """
        traverse JSON object using jsonpath expr, returning values or paths
        /	$	跟节点
        .	@	现行节点
        /	. or []	取子节点
        ..	n/a	就是不管位置，选择所有符合条件的条件
        *	*	匹配所有元素节点
        []	[]	迭代器标示(可以在里面做简单的迭代操作，如数组下标，根据内容选值等)
        &#124	[,]	支持迭代器中做多选
        []	?()	支持过滤操作
        n/a	()	支持表达式计算
        ()	n/a	分组，JsonPath不支持
        """

        def s(x, y):
            """concatenate path elements"""
            return str(x) + ';' + str(y)

        def isint(x):
            """check if argument represents a decimal integer"""
            return x.isdigit()

        def as_path(path):
            """convert internal path representation to
               "full bracket notation" for PATH output"""
            p = '$'
            for piece in path.split(';')[1:]:
                # make a guess on how to index
                # XXX need to apply \ quoting on '!!
                if isint(piece):
                    p += "[%s]" % piece
                else:
                    p += "['%s']" % piece
            return p

        def store(path, object):
            if result_type == 'VALUE':
                result.append(object)
            elif result_type == 'IPATH':  # Index format path (Python ext)
                # return list of list of indices -- can be used w/o "eval" or split
                result.append(path.split(';')[1:])
            else:  # PATH
                result.append(as_path(path))
            return path

        def trace(expr, obj, path):
            if debug: print("trace", expr, "/", path)
            if expr:
                x = expr.split(';')
                loc = x[0]
                x = ';'.join(x[1:])
                if debug: print("\t", loc, type(obj))
                if loc == "*":
                    def f03(key, loc, expr, obj, path):
                        if debug > 1: print(r"\tf03", key, loc, expr, path)
                        trace(s(key, expr), obj, path)

                    walk(loc, x, obj, path, f03)
                elif loc == "..":
                    trace(x, obj, path)

                    def f04(key, loc, expr, obj, path):
                        if debug > 1: print(r"\tf04", key, loc, expr, path)
                        if isinstance(obj, dict):
                            if key in obj:
                                trace(s('..', expr), obj[key], s(path, key))
                        else:
                            if key < len(obj):
                                trace(s('..', expr), obj[key], s(path, key))

                    walk(loc, x, obj, path, f04)
                elif loc == "!":
                    def f06(key, loc, expr, obj, path):
                        if isinstance(obj, dict):
                            trace(expr, key, path)

                    walk(loc, x, obj, path, f06)
                elif isinstance(obj, dict) and loc in obj:
                    trace(x, obj[loc], s(path, loc))
                elif isinstance(obj, list) and isint(loc):
                    iloc = int(loc)
                    if debug: print("----->", iloc, len(obj))
                    if len(obj) > iloc:
                        trace(x, obj[iloc], s(path, loc))
                else:
                    # [(index_expression)]
                    if loc.startswith("(") and loc.endswith(")"):
                        if debug > 1: print("index", loc)
                        e = evalx(loc, obj)
                        trace(s(e, x), obj, path)
                        return

                    # ?(filter_expression)
                    if loc.startswith("?(") and loc.endswith(")"):
                        if debug > 1: print("filter", loc)

                        def f05(key, loc, expr, obj, path):
                            if debug > 1: print("f05", key, loc, expr, path)
                            if isinstance(obj, dict):
                                eval_result = evalx(loc, obj[key])
                            else:
                                eval_result = evalx(loc, obj[int(key)])
                            if eval_result:
                                trace(s(key, expr), obj, path)

                        loc = loc[2:-1]
                        walk(loc, x, obj, path, f05)
                        return

                    m = re.match(r'(-?[0-9]*):(-?[0-9]*):?(-?[0-9]*)$', loc)
                    if m:
                        if isinstance(obj, (dict, list)):
                            def max(x, y):
                                if x > y:
                                    return x
                                return y

                            def min(x, y):
                                if x < y:
                                    return x
                                return y

                            objlen = len(obj)
                            s0 = m.group(1)
                            s1 = m.group(2)
                            s2 = m.group(3)

                            # XXX int("badstr") raises exception
                            start = int(s0) if s0 else 0
                            end = int(s1) if s1 else objlen
                            step = int(s2) if s2 else 1

                            if start < 0:
                                start = max(0, start + objlen)
                            else:
                                start = min(objlen, start)
                            if end < 0:
                                end = max(0, end + objlen)
                            else:
                                end = min(objlen, end)

                            for i in xrange(start, end, step):
                                trace(s(i, x), obj, path)
                        return

                    # after (expr) & ?(expr)
                    if loc.find(",") >= 0:
                        # [index,index....]
                        for piece in re.split(r"'?,'?", loc):
                            if debug > 1: print("piece", piece)
                            trace(s(piece, x), obj, path)
            else:
                store(path, obj)

        def walk(loc, expr, obj, path, funct):
            if isinstance(obj, list):
                for i in xrange(0, len(obj)):
                    funct(i, loc, expr, obj, path)
            elif isinstance(obj, dict):
                for key in obj:
                    funct(key, loc, expr, obj, path)

        def evalx(loc, obj):
            """eval expression"""
            if debug: print("evalx", loc)
            # a nod to JavaScript. doesn't work for @.name.name.length
            # Write len(@.name.name) instead!!!
            loc = loc.replace("@.length", "len(__obj)")
            loc = loc.replace("&&", " and ").replace("||", " or ")

            # replace !@.name with 'name' not in obj
            # XXX handle !@.name.name.name....
            def notvar(m):
                return "'%s' not in __obj" % m.group(1)

            loc = re.sub(r"!@\.([a-zA-Z@_0-9-]*)", notvar, loc)

            # replace @.name.... with __obj['name']....
            # handle @.name[.name...].length
            def varmatch(m):
                def brackets(elts):
                    ret = "__obj"
                    for e in elts:
                        if isint(e):
                            ret += "[%s]" % e  # ain't necessarily so
                        else:
                            ret += "['%s']" % e  # XXX beware quotes!!!!
                    return ret

                g1 = m.group(1)
                elts = g1.split('.')
                if elts[-1] == "length":
                    return "len(%s)" % brackets(elts[1:-1])
                return brackets(elts[1:])

            loc = re.sub(r'(?<!\\)(@\.[a-zA-Z@_.0-9]+)', varmatch, loc)
            # removed = -> == translation
            # causes problems if a string contains =
            # replace @  w/ "__obj", but \@ means a literal @
            loc = re.sub(r'(?<!\\)@', "__obj", loc).replace(r'\@', '@')
            if not use_eval:
                if debug: print("eval disabled")
                raise Exception("eval disabled")
            if debug: print("eval", loc)
            try:
                # eval w/ caller globals, w/ local "__obj"!
                v = eval(loc, caller_globals, {'__obj': obj})
            except Exception as e:
                if debug: print(repr(e))
                return False

            if debug: print("->", v)
            return v

        # body of jsonpath()
        # Get caller globals so eval can pick up user functions!!!
        caller_globals = sys._getframe(1).f_globals
        result = []
        if expr and obj:
            cleaned_expr = self.normalize(expr)
            if cleaned_expr.startswith("$;"):
                cleaned_expr = cleaned_expr[2:]
            # XXX wrap this in a try??
            trace(cleaned_expr, obj, '$')
            if len(result) > 0:
                return result
        return False

JsonPath = JsonPath()
HtmlPath = HtmlPath()

if __name__ == '__main__':
    # try:
    #     import json        # v2.6
    # except ImportError:
    #     import simplejson as json
    # import sys
    # if len(sys.argv) < 3 or len(sys.argv) > 4:
    #     sys.stdout.write("Usage: jsonpath.py FILE PATH [OUTPUT_TYPE]\n")
    #     sys.exit(1)
    # object = json.load(file(sys.argv[1]))
    # path = sys.argv[2]
    # format = 'VALUE'
    # if len(sys.argv) > 3:
    #     # XXX verify?
    #     format = sys.argv[3]
    # value = find(object, path, format)
    # if not value:
    #     sys.exit(1)
    # f = sys.stdout
    # json.dump(value, f, sort_keys=True, indent=1)
    # f.write("\n")
    # sys.exit(0)


    data = {
            "code": 200,
            "message": "success",
            "data": [
                {
                    "year": 2016,
                    "months": [
                        {
                            "url": "https://blog.csdn.net/qq_38795430/article/month/2020/07",
                            "count": 1,
                            "month": "07"
                        },
                        {
                            "url": "https://blog.csdn.net/qq_38795430/article/month/2020/03",
                            "count": 2,
                            "month": "03"
                        },
                        {
                            "url": "https://blog.csdn.net/qq_38795430/article/month/2020/01",
                            "count": 1,
                            "month": "01"
                        }
                    ],
                    "count": 4,
                    "currentYear": False
                },
                {
                    "year": 2017,
                    "months": [
                        {
                            "url": "https://blog.csdn.net/qq_38795430/article/month/2019/09",
                            "count": 6,
                            "month": "09"
                        },
                        {
                            "url": "https://blog.csdn.net/qq_38795430/article/month/2019/08",
                            "count": 3,
                            "month": "08"
                        },
                        {
                            "url": "https://blog.csdn.net/qq_38795430/article/month/2019/07",
                            "count": 5,
                            "month": "07"
                        },
                        {
                            "url": "https://blog.csdn.net/qq_38795430/article/month/2019/06",
                            "count": 1,
                            "month": "06"
                        }
                    ],
                    "count": 29,
                    "currentYear": False
                },
                {
                    "years": 2018,
                    "months": [
                        {
                            "url": "https://blog.csdn.net/qq_38795430/article/month/2018/10",
                            "count": 2,
                            "month": "10"
                        }
                    ],
                    "count": 2,
                    "currentYear": False
                }
            ]
        }
    # 获取month的所有值
    print("获取month的所有值："+str(JsonPath.find(data, '$..month')))

    # 获取data下面所有元素
    print("获取data下面所有元素："+str(JsonPath.find(data, "$.data")))
    print("获取data下面所有元素："+str(JsonPath.find(data, "$.data.*")))

    # 获取data下面所有year的值
    print("获取data下面所有year的值："+str(JsonPath.find(data, "$.data[*].year")))
    print("获取data下面所有year的值："+str(JsonPath.find(data, "$.data..year")))

    # 获取data第1列所有数据
    print("获取data第1列所有数据："+str(JsonPath.find(data, "$.data[0]")))

    # 获取第2~3列所有数据
    print("获取data第2~3列所有数据："+str(JsonPath.find(data, "$.data[1:2]")))

    # 获取data最后一列数据
    print("获取data最后一列数据："+str(JsonPath.find(data, "$.data[(@.length-1)]")))

    # 获取包含了years且条件的数据
    print("获取包含了years且等于2018的数据："+str(JsonPath.find(data, "$.data[?(@.years==2018)]")))
    print("获取包含了years且≥2018的数据："+str(JsonPath.find(data, "$.data[?(@.years>=2018)]")))
    print("获取包含了year且<2018的数据："+str(JsonPath.find(data, "$.data[?(@.year<2017)]")))
    test_str = '获取包含了year且<2018的数'
    print(HtmlPath.border(sum_str=test_str, left_str="获取", right_str="year"))