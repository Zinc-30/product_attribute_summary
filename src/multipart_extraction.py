#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-11-25 17:20
# @Author  : hxinaa
from sys import argv

import pke
import string
from nltk.corpus import stopwords
import os
import json

def multipart_extract(config):
    infile = os.path.join(config['data_dir'], config['doc_files'][0])
    outfile = os.path.join(config['output_dir'], config['doc_files'][0] + '_multipart.keywords')
    print(infile)
    print(outfile)
    # 1. create a MultipartiteRank extractor.
    extractor = pke.unsupervised.MultipartiteRank()

    # 2. load the content of the document.
    extractor.load_document(input=infile)

    # 3. select the longest sequences of nouns and adjectives, that do
    #    not contain punctuation marks or stopwords as candidates.
    pos = {'NOUN', 'PROPN', 'ADJ'}
    stoplist = list(string.punctuation)
    stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
    stoplist += stopwords.words('english')
    extractor.candidate_selection(pos=pos, stoplist=stoplist)

    # 4. build the Multipartite graph and rank candidates using random walk,
    #    alpha controls the weight adjustment mechanism, see TopicRank for
    #    threshold/method parameters.
    extractor.candidate_weighting(alpha=1.1,
                                  threshold=0.74,
                                  method='average')

    # 5. get the 10-highest scored candidates as keyphrases

    keyphrases = extractor.get_n_best(n=config['number'])
    print(keyphrases)
    with open(outfile, "w", encoding='utf-8') as fout:
        for kp in keyphrases:
            fout.write(kp[0] + '\n')

if __name__ == '__main__':
    # import spacy
    # nlp = spacy.load('en_core_web_sm')
    # nlp.max_length = 1030000

    config_file = "../config/default.json"
    with open(config_file) as file:
        config = json.load(file)
    multipart_extract(config)