#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-25

import gensim
from gensim import models
from gensim.models import word2vec
import numpy as np
import jieba.posseg as pseg
import os
import codecs
import pandas as pd

class SimWordVec(object):
    def __init__(self):
        self.embedding_path = '../data/word2vec.model'
        # self.model = gensim.models.KeyedVectors.load_word2vec_format(self.embedding_path, binary=False)
        self.model = models.Word2Vec.load(self.embedding_path)

    '''获取词向量'''
    def get_wordvector(self, word):#获取词向量
        try:
            return self.model[word].reshape(1, 200)
        except:
            return np.zeros(200)
    '''基于余弦相似度计算句子之间的相似度，句子向量等于字符向量求平均'''
    def similarity_cosine(self, word_list1,word_list2):#给予余弦相似度的相似度计算
        vector1 = np.zeros(200)
        for word in word_list1:
            vector1 = np.add(vector1, self.get_wordvector(word))
            # vector1 += self.get_wordvector(word)
        vector1=vector1/len(word_list1)
        vector2=np.zeros(200)
        for word in word_list2:

            vector2 += self.get_wordvector(word)
        vector2=vector2/len(word_list2)
        cos1 = np.sum(vector1*vector2)
        cos21 = np.sqrt(sum(vector1**2))
        cos22 = np.sqrt(sum(vector2**2))
        if cos21*cos22 == 0:
            return 0
        else:
            similarity = cos1/float(cos21*cos22)
            return  similarity
    '''计算句子相似度'''
    def distance(self, text1, text2):#相似性计算主函数
        word_list1=[word.word for word in pseg.cut(text1) if word.flag[0] not in ['w','x','u']]
        word_list2=[word.word for word in pseg.cut(text2) if word.flag[0] not in ['w','x','u']]
        return self.similarity_cosine(word_list1,word_list2)

class BuildModel(object):
    # 对一篇文章分词、去停用词
    def tokenization(self, text, stop_words, stop_flag):
        result = []
        words = pseg.cut(text)
        for word, flag in words:
            if flag not in stop_flag and word not in stop_words:
                result.append(word)
        return result

    def build_model(self):
        # 构建停用词
        stop_words_path = "../data/combined_stopwords.txt"
        stop_words = codecs.open(stop_words_path, 'r', encoding='utf8').readlines()
        stop_words = [w.strip() for w in stop_words]

        # 结巴分词后的停用词性 [标点符号、连词、助词、副词、介词、时语素、‘的’、数词、方位词、代词]
        stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']

        train_data = pd.read_csv('../data/sim_sentence_train.csv')
        M = len(train_data)
        corpus = []
        for i in range(M):
            corpus.append(self.tokenization(train_data['sentence1'][i], stop_words, stop_flag))
            corpus.append(self.tokenization(train_data['sentence2'][i], stop_words, stop_flag))
        model = word2vec.Word2Vec(corpus, size=150)

        # 保存模型，供以后使用
        model.save("../data/word2vec.model")