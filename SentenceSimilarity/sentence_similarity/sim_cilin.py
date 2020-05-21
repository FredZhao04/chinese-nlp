#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-21

import codecs
import jieba.posseg as pseg
import pandas as pd

class SimCilin:

    def __init__(self):
        self.cilin_path = 'data/cilin.txt'
        self.sem_dict = self.load_semantic()

    '''加载语义词典'''
    def load_semantic(self):
        sem_dict = {}
        for line in codecs.open(self.cilin_path):
            line = line.strip().split(' ')
            sem_type = line[0]
            words = line[1:]
            for word in words:
                if word not in sem_dict:
                    sem_dict[word] = sem_type
                else:
                    sem_dict[word] += ';' + sem_type

        for word, sem_type in sem_dict.items():
            sem_dict[word] = sem_type.split(';')
        return sem_dict

    '''比较计算词语之间的相似度，取max最大值'''
    def compute_word_sim(self, word1 , word2):
        if word1 == word2:
            return 1
        sems_word1 = self.sem_dict.get(word1, [])
        sems_word2 = self.sem_dict.get(word2, [])
        score_list = [self.compute_sem(sem_word1, sem_word2) for sem_word1 in sems_word1 for sem_word2 in sems_word2]
        if score_list:
            return max(score_list)
        else:
            return 0

    '''基于语义计算词语相似度'''
    def compute_sem(self, sem1, sem2):
        sem1 = [sem1[0], sem1[1], sem1[2:4], sem1[4], sem1[5:7], sem1[-1]]
        sem2 = [sem2[0], sem2[1], sem2[2:4], sem2[4], sem2[5:7], sem2[-1]]
        score = 0
        for index in range(len(sem1)):
            if sem1[index] == sem2[index]:
                if index in [0, 1]:
                    score += 3
                elif index == 2:
                    score += 2
                elif index in [3, 4]:
                    score += 1
        return score/10

    '''基于词相似度计算句子相似度'''
    def distance(self, sentence1, sentence2):
        words1 = [word.word for word in pseg.cut(sentence1) if word.flag[0] not in ['u', 'x', 'w']]
        words2 = [word.word for word in pseg.cut(sentence2) if word.flag[0] not in ['u', 'x', 'w']]
        score_words1 = []
        score_words2 = []
        for word1 in words1:
            score = max(self.compute_word_sim(word1, word2) for word2 in words2)
            score_words1.append(score)
        for word2 in words2:
            score = max(self.compute_word_sim(word2, word1) for word1 in words1)
            score_words2.append(score)
        similarity = max(sum(score_words1)/len(words1), sum(score_words2)/len(words2))

        return similarity


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


    # test()
    # train_data = pd.read_csv("data/atec_nlp_sim_train.csv", header=None)
    # # 102475 条数据
    # result = pd.DataFrame()
    # sentence1 = []
    # sentence2 = []
    # label = []
    # for i in range(len(train_data)):
    #     t = str(train_data.iloc[i,0]).split('\t')
    #     if len(t) > 3:
    #         sentence1.append(t[1])
    #         sentence2.append(t[2])
    #         label.append(t[3])
    # result['sentence1'] = sentence1
    # result['sentence2'] = sentence2
    # result['label'] = label
