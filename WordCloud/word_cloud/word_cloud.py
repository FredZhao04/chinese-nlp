#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xining Zhao
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import jieba.posseg as pseg
import os
import collections
import numpy as np
from string import punctuation
import re
import wordcloud # 词云展示库
from PIL import Image # 图像处理库
import matplotlib.pyplot as plt
import conf
from segmentation import WordSegmentation

def get_default_wc_background():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'wc.png')

def get_default_wc_save_path():
    save_path = os.path.dirname(os.path.realpath(__file__))
    return save_path

def get_default_wc_name():
    return "word_cloud.png"

def get_default_font_path():
    file_path = os.path.dirname(os.path.realpath(__file__))
    font_path = os.path.join(file_path, "SimHei.ttf")
    return font_path

class WordCloud(object):

    def __init__(self, stop_words_file = None,
                 allow_speech_tags = conf.allow_speech_tags,
                 wc_background = None,
                 font_path = None,
                 max_words = 200,
                 max_font_size = 100,
                 save_path = None,
                 wc_name = None,
                 topK = 10):
        """
        :param stop_words_file:  -- str，停用词文件路径，若不是str则使用默认停用词文件
        :param allow_speech_tags:  -- 词性列表
        :param wc_background: 词云图背景图片
        :param max_words: 最多显示词数，默认200
        :param max_font_size: 字体最大值，默认100
        :param save_path: 词云图保存地址，默认当前文件夹
        """
        self.seg = WordSegmentation(stop_words_file=stop_words_file,
                                    allow_speech_tags=allow_speech_tags)
        self.wc_background = get_default_wc_background()
        if type(wc_background) is str:
            self.wc_background = wc_background
        self.font_path = get_default_font_path()
        if type(font_path) is str:
            self.font_path = font_path
        self.max_words = max_words
        self.max_font_size = max_font_size
        self.save_path = get_default_wc_save_path()
        if type(save_path) is str:
            self.save_path = save_path
        self.wc_name = get_default_wc_name()
        if type(wc_name) is str:
            self.wc_name = wc_name + '.png'
        self.topK = topK

    def del_punctuation(self, str):
        """
        去除 英文标点符号+中文标点符号
        :param str:
        :return: str
        """
        punc = punctuation + u'.,;《》？！“”‘’@#￥%…&×（）——+【】{};；●，。&～、|\s:：\n'
        res = re.sub(r"[{}]+".format(punc), "", str)
        return res

    def tokenization(self, text):
        """
        对一篇文章分词、去停用词
        :return:
        """
        text_clean = self.del_punctuation(text)
        result = []
        words = pseg.cut(text_clean)
        stop_words = self.seg.stop_words
        for word, flag in words:
            if flag in self.seg.default_speech_tag_filter and word not in stop_words:
                result.append(word)
        return result

    def create_word_cloud(self, text):
        """

        :param word_list: 经过去除标点符号、分词、去停用词后的词列表
        :return:
        """
        word_list = self.tokenization(text)
        word_counts = collections.Counter(word_list)  # 对分词做词频统计
        word_counts_topK = word_counts.most_common(self.topK)  # 获取前K最高频的词
        # print(word_counts_topK)
        # 词频展示
        mask = np.array(Image.open(self.wc_background))  # 定义词频背景
        wc = wordcloud.WordCloud(
            font_path=self.font_path,  # 设置字体格式
            mask=mask,  # 设置背景图
            max_words=self.max_words,  # 最多显示词数
            max_font_size=self.max_font_size  # 字体最大值
        )

        wc.generate_from_frequencies(word_counts)  # 从字典生成词云
        image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
        wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
        plt.imshow(wc)  # 显示词云
        plt.axis('off')  # 关闭坐标轴
        plt.savefig(os.path.join(self.save_path, self.wc_name))
        plt.show()  # 显示图像

