# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-27

import os
from datasketch import MinHash, MinHashLSH
from nltk import ngrams

class SimMinhash(object):
    """根据不同文件情况修改文件读取函数"""
    # 读取文件正文
    # def read_file(self, file_path):
    #     with open(file_path, 'r', encoding="gbk") as f:
    #         lines = f.readlines()
    #         flag = False
    #         content = ''
    #         for line in lines:
    #             if line.startswith("【 标  题 】"):
    #                 # print(line.strip())
    #                 pass
    #             if line.startswith("【 正  文 】"):
    #                 flag = True
    #             if flag:
    #                 content += line.strip()
    #     return content.strip("【 正  文 】")
    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            content = ''
            for line in lines:
                content += line.strip()
        return content

    """需要把语料库路径可配置化"""
    def create_data(self):
        data = []
        # base_dir = '../data/train/C3-Art/'
        base_dir = '../data/gov_files/'
        files = os.listdir(base_dir)
        for file in files:
            file_path = os.path.join(base_dir, file)
            try:
                content = self.read_file(file_path)
                data.append({'file_name': file, 'content': content})
            except:
                pass
        return data

    """参数可匹配化"""
    def get_most_similar(self, threshold=0.8, num_perm=128, ngrams_num=3):
        lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)

        minhashes = {}
        data = self.create_data()
        for single_data in data:
            minhash = MinHash(num_perm=num_perm)
            file_name = single_data['file_name']
            content = single_data['content']
            for d in ngrams(content, ngrams_num):
                minhash.update("".join(d).encode('utf-8'))
            lsh.insert(file_name, minhash)
            minhashes[file_name] = minhash
        for file_name in minhashes.keys():
            result = lsh.query(minhashes[file_name])
            # 排除自身文件，若存在相似度大于0.5，则打印
            result.remove(file_name)
            if len(result) > 0:
                print("Candidates with Jaccard similarity > 0.8 for input ", file_name, ":", result)
