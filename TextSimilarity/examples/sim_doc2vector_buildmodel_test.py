#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-28

from TextSimilarity.text_similarity.sim_doc2vector import Doc2VectorBuildModel

if __name__=="__main__":
    dv = Doc2VectorBuildModel()
    dv.build_model()