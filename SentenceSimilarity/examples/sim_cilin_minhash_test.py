#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-26

import pandas as pd
from SentenceSimilarity.sentence_similarity.sim_cilin import SimCilin
from SentenceSimilarity.sentence_similarity.sim_minhash import SimJaccard
from time import *

if __name__=="__main__":
    begin_time = time()
    # 1、首先构建word2vecrtor的模型model
    # 构建model耗时： 174.84s
    # bm = BuildModel()
    # bm.build_model()
    # 2、进行测试
    train_data = pd.read_csv('../data/sim_sentence_train.csv')
    M = 10000 #len(train_data)
    N = 0
    total = 0
    simer_cilin = SimCilin()
    simer_minhash = SimJaccard()
    for i in range(M):
        sentence1 = train_data['sentence1'][i]
        sentence2 = train_data['sentence2'][i]
        lable = train_data['label'][i]

        sim1 = simer_minhash.distance(sentence1, sentence2)
        sim2 = simer_cilin.distance(sentence1, sentence2)
        sim = sim1*0.5 + sim2*0.5
        # 测试负样本准确率
        # if lable == 0:
        #     total += 1
        #     if sim < 0.5:
        #         N += 1
        # 测试正样本准确率
        # if lable == 1:
        #     total += 1
        #     if sim >= 0.5:
        #         N += 1
        # 总体准确率
        if (sim >= 0.5 and lable == 1) or (sim < 0.5 and lable == 0):
            N += 1

        if i % 1000 == 0:
            print("************程序运行到 %d 条**************" % i)

    print("准确率为: %f " % (N/M))

    end_time = time()
    print('该程序运行时间：',(end_time - begin_time))