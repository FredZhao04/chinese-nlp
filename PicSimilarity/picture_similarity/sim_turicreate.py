#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-6-3

import turicreate as tc

data  = tc.image_analysis.load_images('../data/')
data = data.add_row_number()

model = tc.image_similarity.create(data)
# tc.Image(data[0]['path']).show()

similar_images = model.query(data[0:1], k=10)

similar_image_index = similar_images['reference_label'][1:]

filtered_index = data['id'].apply(lambda x : x in similar_image_index)

data[filtered_index].explore()