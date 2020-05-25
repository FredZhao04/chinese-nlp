#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-25

import pandas as pd
from SentenceSimilarity.sentence_similarity.sim_wordvector import BuildModel, SimWordVec
from time import *

if __name__=="__main__":
    begin_time = time()
    # 1、首先构建word2vecrtor的模型model
    # 构建model耗时： 174.84s
    # bm = BuildModel()
    # bm.build_model()
    # 2、进行测试
    train_data = pd.read_csv('../data/sim_sentence_train.csv')
    M = len(train_data)
    N = 0
    for i in range(M):
        sentence1 = train_data['sentence1'][i]
        sentence2 = train_data['sentence2'][i]
        lable = train_data['label'][i]

        simer = SimWordVec()
        sim = simer.distance(sentence1, sentence2)
        if sim >= 0.5:
            sim = 1
        else:
            sim = 0

        if sim == lable:
            N += 1

        if i % 1000 == 0:
            print("************程序运行到 %d 条**************" % i)

    print("准确率为: %f " % (N/M))

    end_time = time()
    print('该程序运行时间：',(end_time - begin_time))