#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-11-25 17:23
# @Author  : hxinaa
from sys import argv
import pke
from nltk.corpus import stopwords
import json
import os
import tqdm
from tfidf import caculate_freq
from pathlib import Path


def kea_extract(config):
    stoplist = stopwords.words('english')
    extractor = pke.supervised.Kea()
    caculate_freq(config, stopwords.words('english'))
    output_dir = Path(config['output_dir'])
    input_total = output_dir.joinpath('tfidf_source/')
    out_freq = input_total.joinpath('doc_freq.tsv.gz')
    for item in tqdm.tqdm(config['doc_files']):
        infile = os.path.join(config['data_dir'],item)
        outfile = os.path.join(config['output_dir'], item + '_kea.keywords')
        print(outfile)
        # define a list of stopwords
        # 2. load the content of the document.
        extractor.load_document(input=infile,
                                language='en',
                                normalization=None)
        # 3. select 1-3 grams that do not start or end with a stopword as
        #    candidates. Candidates that contain punctuation marks as words
        #    are discarded.
        extractor.candidate_selection(stoplist=stoplist)

        # 4. classify candidates as keyphrase or not keyphrase.
        df = pke.load_document_frequency_file(input_file=str(out_freq))
        extractor.candidate_weighting(model_file=None, df=df)

        keyphrases = extractor.get_n_best(n=config['number'])
        print(keyphrases)
        with open(outfile, "w", encoding='utf-8') as fout:
            for kp in keyphrases:
                fout.write(kp[0] + '\n')


if __name__ == '__main__':
    config_file = "../config/all_beauty.json"
    with open(config_file) as file:
        config = json.load(file)
    kea_extract(config)
