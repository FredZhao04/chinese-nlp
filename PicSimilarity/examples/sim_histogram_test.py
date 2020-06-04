#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-6-4

from PicSimilarity.picture_similarity.sim_histogram import SimHistogram
import cv2

if __name__ == '__main__':
    sh = SimHistogram()
    img1_path = '../data/walle/image-001.jpeg'
    img2_path = '../data/walle/image-014.jpeg'
    # 读取图片内容
    img1 = cv2.imread(img1_path)
    # 读取图片内容
    img2 = cv2.imread(img2_path)

    sim = sh.compare_similar_hist(sh.calc_bgr_hist(img1), sh.calc_bgr_hist(img2))
    print(sim)