#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-28

from TextSimilarity.text_similarity.sim_doc2vector import SimDoc2Vector
from gensim.models.doc2vec import Doc2Vec

if __name__=="__main__":
    test_data_1 = '图书评论是近代报刊业兴起后，在世界各国得到长足发展的一种新型评论体裁。而不论是书评理论还是书评实践都有一个不小的疏漏，即忽\
    视了图书的形式因素。因为图书是内容与形式的综合体，忽视了“图书形式”这一重要方面，会导致在图书评论活动中忽视对图书的出版形式这一重要方面的品评论述，而这对于出版物的达到基本要求：“形神俱佳”（“形”指书装艺术，“神”指内容叙述）或最高要求“尽善尽美”（“尽善”指内容而言，“尽美”指形式而言）无疑是有缺憾的。'
    model = Doc2Vec.load("../data/model/doc2vec.model")
    dv = SimDoc2Vector()
    dv.get_most_similar(model, test_data_1)


