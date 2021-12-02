#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-12-02 13:08
# @Author  : hxinaa
from sys import argv
import logging
from selection import selection
from metrics.metrics import *
from autophrase_extraction import autophrase_extraction
from positionrank_extraction import positionrank_extract
from textrank import TextRank

import pandas as pd
import json
import os
config = json.load(open('../config/default.json'))

def generate(item):
    config['doc_files'] = ["reviews_Musical_Instruments_5_item_{}.txt".format(item)]
    autophrase_extraction(config)
    # positionrank_extract(config)
    # TextRank(config)



def eval(itemlist,methods):
    """

    :param itemlist: a list of item to check
    :param methods: a list of keyphrase extraction methods

    :return: results
    """
    result = []
    row = {}

    for item in itemlist:
        ans_file = "../label/reviews_Musical_Instruments_5_item_{}.txt".format(item)
        # print(ans_file)
        ans_list = []
        if os.path.exists(ans_file):
            row['item'] = item
            for line in open(ans_file):
                ans_list.append(line.strip())
            row['ans'] = ans_list
            # print(ans_list)
        else:
            continue
        for m in methods:
            out_file = "../output/reviews_Musical_Instruments_5_item_{}.txt_{}.keywords".format(item,m)
            # print(out_file)
            out_list = []
            if os.path.exists(out_file):
                row['method'] = m
                for line in open(out_file):
                    out_list.append(line.strip())
                out_list_pruned = selection(out_list)
                row['out'] = out_list
                row['out_pruned'] = out_list_pruned
                row['bpref'] = bpref(ans_list,out_list)
                row['bpref_p'] = bpref(ans_list,out_list_pruned)
                row['mrr'] = mrr(ans_list, out_list)
                row['mrr_p'] = mrr(ans_list, out_list_pruned)
                # row['p@1'] = precision_at_k_batch(ans_list, out_list,1)
                # row['p_pruned@1'] = precision_at_k_batch(ans_list, out_list_pruned,1)
            else:
                continue
        result.append(row)
    df = pd.DataFrame(result)
    df.to_csv('../label/result.csv')

if __name__ == '__main__':
    methods = ['autophrase','kea','kpminer','posrank','topicrank','topicalrank','yake']
    items = ['B000068O3D','B000068O3X','B000068O4H','B000068O59','B00006LVEU']
    # for item in items:
    #     generate(item)
    eval(items,methods)





