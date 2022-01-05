#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-12-09 13:11
# @Author  : hxinaa
from sys import argv
import logging
import gzip
import json
def build_qualitydata(file):
    ans = set([])
    gfile = gzip.open(file, 'r')
    for line in gfile:
        # print(line)
        x = json.loads(line)
        if 'feature' in x:
            for phrases in x[u'feature']:
                if len(phrases.split(" ")) > 5:
                    continue
                ans.add(phrases)
if __name__ == '__main__':
    quality_data = build_qualitydata('../data/All_Amazon_Meta.json.gz')
    with open('../data/amazon_quality.txt','w') as fout:
        for x in quality_data:
            fout.write(x+'\n')