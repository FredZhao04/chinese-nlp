#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-6-3

import hashlib

class GenerateHash(object):
    """
    输入(二进制)文本，输出该文本的hash值
    对于相同的文本，会输出相同的hash值
    """
    def __init__(self):
        pass

    # SHA1散列函数
    def create_sha1(self, text):
        sha1obj = hashlib.sha1()
        sha1obj.update(text)
        hash = sha1obj.hexdigest()
        return hash

    # MD5散列函数
    def create_md5(self, text):
        md5obj = hashlib.md5()
        md5obj.update(text)
        hash = md5obj.hexdigest()
        return hash