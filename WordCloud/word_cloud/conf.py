#!/usr/bin/env python3
# coding: utf-8

# Author: Xining Zhao
# Date: 2020-5-21


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

sentence_delimiters = ['?', '!', ';', '？', '！', '。', '；', '……', '…', '\n']
allow_speech_tags = ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns', 'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']

text_type    = str
string_types = (str,)
xrange       = range

def as_text(v):  ## 生成unicode字符串
    if v is None:
        return None
    elif isinstance(v, bytes):
        return v.decode('utf-8', errors='ignore')
    elif isinstance(v, str):
        return v
    else:
        raise ValueError('Unknown type %r' % type(v))

def is_text(v):
    return isinstance(v, text_type)



if __name__ == '__main__':

    pass

