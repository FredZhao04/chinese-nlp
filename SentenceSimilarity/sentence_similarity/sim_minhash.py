#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-22

import jieba.posseg as pseg
from datasketch import MinHash

class SimJaccard(object):
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    '''对全文进行分词,提取全文特征,使用词性将虚词等无关字符去重'''
    def get_features(self, string):
        word_list=[word.word for word in pseg.cut(string) if word.flag[0] not in ['u','x','w','o','p','c','m','q']]
        return word_list

    '''计算s1与s2之间的距离'''
    def distance(self, s1, s2):
        word_list1 = self.get_features(s1)
        word_list2 = self.get_features(s2)
        m1, m2 = MinHash(), MinHash()
        for d in word_list1:
            m1.update(d.encode('utf8'))
        for d in word_list2:
            m2.update(d.encode('utf8'))
        return m1.jaccard(m2)