#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-6-5
import cv2

class SimDhash(object):
    """差值感知算法"""
    def __init__(self, size=(65, 64)):
        self.size = size

    def getHashCode(self, img):
        # 缩放图像
        img = cv2.resize(img, self.size, interpolation=cv2.INTER_CUBIC)
        # 转换为灰度图
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        result = []
        # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
        for i in range(self.size[0] - 1):
            for j in range(self.size[1]):
                if gray[i, j] > gray[i, j + 1]:
                    result.append(1)
                else:
                    result.append(0)

        return result

    # 比较hash值
    def compHashCode(self, hc1, hc2):
        cnt = 0
        for i, j in zip(hc1, hc2):
            if i == j:
                cnt += 1
        return cnt

    # 计算平均哈希算法相似度
    def calaHashSimilarity(self, img1, img2):
        hc1 = self.getHashCode(img1)
        hc2 = self.getHashCode(img2)
        same_count = self.compHashCode(hc1, hc2)
        similarity = same_count / ((self.size[0]-1)*self.size[1])
        return similarity
