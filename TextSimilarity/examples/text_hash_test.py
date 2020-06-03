#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-6-3

from TextSimilarity.text_similarity.text_hash import GenerateHash

# 读取文件,二进制形式
def read_file(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    return content

if __name__ == "__main__":
    hashfile1 = "/Users/fred/Desktop/python-softwares/语料库/train/C3-Art/C3-Art0001.txt"
    hashfile2 = "/Users/fred/Desktop/python-softwares/语料库/train/C3-Art/C3-Art1481.txt"
    hashfile3 = "/Users/fred/Desktop/python-softwares/语料库/train/C3-Art/C3-Art1482.txt"
    text1 = read_file(hashfile1)
    text2 = read_file(hashfile2)
    text3 = read_file(hashfile3)
    gh = GenerateHash()
    # hash1 = gh.create_md5(text1)
    # hash2 = gh.create_md5(text2)
    # hash3 = gh.create_md5(text3)
    # print(hash1)
    # print(hash2)
    # print(hash3)

    hash1 = gh.create_sha1(text1)
    hash2 = gh.create_sha1(text2)
    hash3 = gh.create_sha1(text3)
    print(hash1)
    print(hash2)
    print(hash3)