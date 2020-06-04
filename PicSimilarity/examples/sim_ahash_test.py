#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-6-4

import cv2
from PicSimilarity.picture_similarity.sim_ahash import SimAhash

if __name__=="__main__":
    sa = SimAhash(size=(8, 8))
    img1_path = '../data/walle/image-001.jpeg'
    img2_path = '../data/walle/image-054.jpg'
    # 读取图片内容
    img1 = cv2.imread(img1_path)
    # 读取图片内容
    img2 = cv2.imread(img2_path)
    r = sa.calaHashSimilarity(img1, img2)
    print(r)