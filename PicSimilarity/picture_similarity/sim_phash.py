#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-6-3

import glob
import os
import sys
from functools import reduce

from PIL import Image

class SimPhash(object):
    def __init__(self, size=(64, 64)):
        self.EXTS = ['jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG']
        self.size = size

    def avhash(self, im):
        if not isinstance(im, Image.Image):
            im = Image.open(im)
        im = im.resize(self.size, Image.ANTIALIAS).convert('L')
        avg = reduce(lambda x, y: x + y, im.getdata()) / (self.size[0] * self.size[1])
        return reduce(lambda x, y_z: x | (y_z[1] << y_z[0]),
                      enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                      0)

    def hamming(self, h1, h2):
        h, d = 0, h1 ^ h2
        while d:
            h += 1
            d &= d - 1
        return h

    def get_most_similiar(self, image, file_path):
        """
        :param image: 要比对的图片路径
        :param file_path: 图片库所在的文件夹路径
        :return: list [相似度 \t 图片名]
        """
        h = self.avhash(image)
        os.chdir(file_path)
        images = []
        for ext in self.EXTS:
            images.extend(glob.glob('*.%s' % ext))
        seq = []
        prog = int(len(images) > 50 and sys.stdout.isatty())
        for f in images:
            seq.append((f, 1 - self.hamming(self.avhash(f), h)/(64*64)))
            if prog:
                perc = 100. * prog / len(images)
                x = int(2 * perc / 5)
                print('\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']', )
                print('%.2f%%' % perc, '(%d/%d)' % (prog, len(images)), )
                sys.stdout.flush()
                prog += 1
        return seq
