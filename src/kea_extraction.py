#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-11-25 17:23
# @Author  : hxinaa
from sys import argv
import pke
from nltk.corpus import stopwords
import json
import os

def kea_extract(config):
    infile = os.path.join(config['data_dir'], config['doc_files'][0])
    outfile = os.path.join(config['output_dir'], config['doc_files'][0] + '_kea.keywords')
    print(outfile)
    # define a list of stopwords
    stoplist = stopwords.words('english')

    # 1. create a Kea extractor.
    extractor = pke.supervised.Kea()

    # 2. load the content of the document.
    extractor.load_document(input=infile,
                            language='en',
                            normalization=None)

    # 3. select 1-3 grams that do not start or end with a stopword as
    #    candidates. Candidates that contain punctuation marks as words
    #    are discarded.
    extractor.candidate_selection(stoplist=stoplist)

    # 4. classify candidates as keyphrase or not keyphrase.
    df = pke.load_document_frequency_file(input_file='path/to/df.tsv.gz')
    model_file = 'path/to/kea_model'
    extractor.candidate_weighting(self,
                                  model_file=model_file,
                                  df=df)

    keyphrases = extractor.get_n_best(n=config['number'])
        print(keyphrases)
        with open(outfile, "w", encoding='utf-8') as fout:
            for kp in keyphrases:
                fout.write(kp[0] + '\n')

if __name__ == '__main__':
    config_file = "../config/default.json"
    with open(config_file) as file:
        config = json.load(file)
    multipart_extract(config)