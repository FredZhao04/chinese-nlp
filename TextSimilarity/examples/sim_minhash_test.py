#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-28

from TextSimilarity.text_similarity.sim_minhash import SimMinhash
import  datetime

if __name__=="__main__":
    old_time = datetime.datetime.now()

    simer = SimMinhash()
    simer.get_most_similar()

    print(datetime.datetime.now() - old_time)
