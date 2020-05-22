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
    for i in range(M):
        sentence1 = train_data['sentence1'][i]
        sentence2 = train_data['sentence2'][i]
        lable = train_data['label'][i]

        simer = SimJaccard()
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