#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-6-3
from PicSimilarity.picture_similarity.sim_phash import SimPhash

if __name__=="__main__":
    im = '/Users/fred/Documents/GitHub/chinese-nlp/PicSimilarity/data/walle/image-001.jpeg'
    wd = '/Users/fred/Documents/GitHub/chinese-nlp/PicSimilarity/data/walle/'
    simer = SimPhash()
    seq = simer.get_most_similiar(im, wd)
    for f, ham in sorted(seq, key=lambda i: i[1]):
        print("%d\t%s" % (ham, f))