#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-22

import pandas as pd
from SentenceSimilarity.sentence_similarity.sim_minhash import SimJaccard
from time import *

if __name__=="__main__":
    begin_time = time()
    train_data = pd.read_csv('../data/sim_sentence_train.csv')
    M = len(train_data)
    N = 0
    total = 0
    simer = SimJaccard()
    for i in range(M):
        sentence1 = train_data['sentence1'][i]
        sentence2 = train_data['sentence2'][i]
        lable = train_data['label'][i]
        # if lable == 0:
        #     total += 1
        #     sim = simer.distance(sentence1, sentence2)
        #     if sim < 0.4:
        #         N += 1
        sim = simer.distance(sentence1, sentence2)
        # 测试总体准确率
        if (sim >= 0.5 and lable == 1) or (sim < 0.5 and lable == 0):
            N += 1

        if i % 1000 == 0:
            print("************程序运行到 %d 条**************" % i)
    print("准确率为: %f " % (N /M))
    # print("准确率为: %f " % (N/total))

    end_time = time()
    print('该程序运行时间：',(end_time - begin_time))