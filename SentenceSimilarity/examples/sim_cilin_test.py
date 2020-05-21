#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-21

import pandas as pd

if __name__=="__main__":
    train_data = pd.read_csv('data/sim_sentence_train.csv')
    M = len(train_data)
    N = 0
    for i in range(len(train_data)):
        sentence1 = train_data['sentence1'][i]
        sentence2 = train_data['sentence2'][i]
        lable = train_data['label'][i]

        simer = SimCilin()
        sim = simer.distance(sentence1, sentence2)
        if sim >= 0.5:
            sim = 1
        else:
            sim = 0

        if sim == lable:
            N += 1
    print("准确率为: %f " % (N/M))