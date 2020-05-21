#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-21

from WordCloud.word_cloud.word_cloud import WordCloud

if __name__=="__main__":
    # 读取文件
    with open("../data/test.txt", 'r') as f:
        string_data = f.read()
    wc = WordCloud()
    wc.create_word_cloud(string_data)