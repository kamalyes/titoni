# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# File  : EncryptUtils.py
# Author: YuYanQing
# Desc  : 加解密算法
# Date  : 2020/9/25 19:42
'''
import base64
from hashlib import sha1, md5

class CipherHelper:
    def base64Encrypt(self,key):
        """
        base64 算法加密
        :return:加密后的字符
        Example::
            >>> print(CipherHelper().base64Encrypt("Hello Word base64Encrypt"))
        """
        binary = base64.b64encode(key.encode())
        return binary

    def base64Decrypt(self, binary):
        """
        base64 算法解密
        binary 需要转成2进制格式才可以转换，所以我们这里再手动转换一下
        :return:算解密后的字符
        """
        b64decode = base64.b64decode(binary).decode()
        return b64decode

    def md5Encrypt(self, decode_msg):
        """
        md5 算法加密
        :param decode_msg: 需加密的字符串
        :return: 加密后的字符
        Example::
            >>> print(CipherHelper().md5Encrypt("Hello Word md5Encrypt"))
        """
        hl = md5()
        hl.update(decode_msg.encode('utf-8'))
        return hl.hexdigest()

    def sha1Encrypt(self, decode_msg):
        """
        哈希算法加密
        :param decode_msg: 需加密的字符串
        :return: 加密后的字符
        Example::
            >>> print(CipherHelper().sha1Encrypt("Hello Word sha1Encrypt"))
        """
        sh = sha1()
        sh.update(decode_msg.encode('utf-8'))
        return sh.hexdigest()
