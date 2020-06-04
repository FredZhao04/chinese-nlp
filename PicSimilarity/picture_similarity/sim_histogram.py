#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-6-4

import cv2
from math import sqrt

class SimHistogram(object):
    """
    直方图算法
    """
    def __init__(self):
        pass
    # 颜色映射
    def bgr_mapping(self, img_val):
        # 将bgr颜色分成8个区间做映射
        if img_val >= 0 and img_val <= 31: return 0
        if img_val >= 32 and img_val <= 63: return 1
        if img_val >= 64 and img_val <= 95: return 2
        if img_val >= 96 and img_val <= 127: return 3
        if img_val >= 128 and img_val <= 159: return 4
        if img_val >= 160 and img_val <= 191: return 5
        if img_val >= 192 and img_val <= 223: return 6
        if img_val >= 224: return 7

    # 颜色直方图的数值计算
    def calc_bgr_hist(self, image):
        if not image.size: return False
        hist = {}
        # 缩放尺寸减小计算量
        image = cv2.resize(image, (32, 32))
        for bgr_list in image:
            for bgr in bgr_list:
                # 颜色按照顺序映射
                maped_b = self.bgr_mapping(bgr[0])
                maped_g = self.bgr_mapping(bgr[1])
                maped_r = self.bgr_mapping(bgr[2])
                # 计算像素值
                index = maped_b * 8 * 8 + maped_g * 8 + maped_r
                hist[index] = hist.get(index, 0) + 1

        return hist


    # 计算两张图片的相似度
    def compare_similar_hist(self, h1, h2):
        if not h1 or not h2: return False
        sum1, sum2, sum_mixd = 0, 0, 0
        # 像素值key的最大数不超过512，直接循环到512，遍历取出每个像素值
        for i in range(512):
            # 计算出现相同像素值次数的平方和
            sum1 = sum1 + (h1.get(i, 0) * h1.get(i, 0))
            sum2 = sum2 + (h2.get(i, 0) * h2.get(i, 0))
            # 计算两个图片次数乘积的和
            sum_mixd = sum_mixd + (h1.get(i, 0) * h2.get(i, 0))
        # 按照余弦相似性定理计算相似度
        return sum_mixd / (sqrt(sum1) * sqrt(sum2))


