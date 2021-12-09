#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-12-09 13:11
# @Author  : hxinaa
from sys import argv
import logging
import gzip
def build_qualitydata(file):
    ans = []
    gfile = gzip.open(file, 'r')
    for line in  gfile:
        x = json.load(line)
        if 'feature' in x:
            for phrases in x[u'feature']:
                ans.append(phrases)
    return ans




if __name__ == '__main__':
    quality_data = build_qualitydata('../data/All_Amazon_Meta.json.gz')
    with open('../data/amazon_quality.txt','w') as fout:
        for x in quality_data:
            fout.write(x+'\n')