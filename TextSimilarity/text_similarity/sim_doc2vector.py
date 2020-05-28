# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-27

import jieba.posseg as pseg
import codecs
import os
from gensim.models.doc2vec import TaggedDocument,Doc2Vec

class SimDoc2Vector(object):
    """该functioin可以提取成公共函数"""
    # 对一篇文章分词、去停用词
    def tokenization(self, text, stop_words, stop_flag):
        result = []
        words = pseg.cut(text)
        for word, flag in words:
            if flag not in stop_flag and word not in stop_words:
                result.append(word)
        return result

    def get_most_similar(self, model, text, topK=5):
        """停用词获取可以提取成公共函数"""
        # 构建停用词
        stop_words_path = "../data/combined_stopwords.txt"
        stop_words = codecs.open(stop_words_path, 'r', encoding='utf8').readlines()
        stop_words = [w.strip() for w in stop_words]

        # 结巴分词后的停用词性 [标点符号、连词、助词、副词、介词、时语素、‘的’、数词、方位词、代词]
        stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']

        word_list = self.tokenization(text, stop_words, stop_flag)
        inferred_vector = model.infer_vector(word_list)
        sims = model.docvecs.most_similar([inferred_vector], topn=topK)
        print(sims)  # sims是一个tuples,(index_of_document, similarity)
        for i in sims:
            similar = ""
            print('################################')
            print(i[0])
            # for j in doc[i[0]]:
            #     similar += j
            # print(similar)

class Doc2VectorBuildModel(object):
    # 对一篇文章分词、去停用词
    def tokenization(self, text, stop_words, stop_flag):
        result = []
        words = pseg.cut(text)
        for word, flag in words:
            if flag not in stop_flag and word not in stop_words:
                result.append(word)
        return result

    """根据不同文件情况修改文件读取函数"""
    # 读取文件正文
    def read_file(self, file_path):
        with open(file_path, 'r', encoding="gbk") as f:
            lines = f.readlines()
            flag = False
            content = ''
            for line in lines:
                if line.startswith("【 标  题 】"):
                    # print(line.strip())
                    pass
                if line.startswith("【 正  文 】"):
                    flag = True
                if flag:
                    content += line.strip()
        return content.strip("【 正  文 】")

    def build_model(self):
        # 构建停用词
        stop_words_path = "../data/combined_stopwords.txt"
        stop_words = codecs.open(stop_words_path, 'r', encoding='utf8').readlines()
        stop_words = [w.strip() for w in stop_words]

        # 结巴分词后的停用词性 [标点符号、连词、助词、副词、介词、时语素、‘的’、数词、方位词、代词]
        stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']

        # 读取文件正文
        base_dir = '../data/train/C3-Art/'
        files = os.listdir(base_dir)
        raw_documents = []
        for file in files:
            file_path = os.path.join(base_dir, file)
            try:
                title = file_path
                content = self.read_file(file_path)
                raw_documents.append(title + '\n' + content)
            except:
                pass

        # 构建语料库
        corpora_documents = []
        doc = []  # 输出时使用，用来存储未经过TaggedDocument处理的数据，如果输出document，前面会有u
        for i, item_text in enumerate(raw_documents):
            words_list = self.tokenization(item_text, stop_words, stop_flag)
            document = TaggedDocument(words=words_list, tags=[i])
            corpora_documents.append(document)
            doc.append(words_list)
        # 创建model
        model = Doc2Vec(vector_size=50, min_count=1)
        model.build_vocab(corpora_documents)
        model.train(corpora_documents, epochs=20, total_examples=model.corpus_count)

        # 保存模型，供以后使用
        model.save("../data/model/doc2vec.model")