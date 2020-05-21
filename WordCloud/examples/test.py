#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xining Zhao
"""

from word_cloud import WordCloud

if __name__=="__main__":
    # 读取文件
    with open("../data/test.txt", 'r') as f:
        string_data = f.read()
    wc = WordCloud()
    wc.create_word_cloud(string_data)