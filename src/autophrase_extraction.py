#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-11-16 20:47
# @Author  : hxinaa
from sys import argv
import json
import pandas as pd
from autophrasex import *
import os

def autophrase_extraction(config):
	autophrase = AutoPhrase(
		reader=DefaultCorpusReader(tokenizer=JiebaTokenizer()),
		selector=DefaultPhraseSelector(),
		extractors=[
			NgramsExtractor(N=6),
			IDFExtractor(),
			EntropyExtractor()
		]
	)

	# extraction
	predictions = autophrase.mine(
		corpus_files=[os.path.join(config['data_dir'],f) for f in config['doc_files']],
		quality_phrase_files=os.path.join(config['data_dir'],config['quality_file']),
		callbacks=[
			LoggingCallback(),
			ConstantThresholdScheduler(),
			EarlyStopping(patience=2, min_delta=3)
		])

	sorted_predictions = sorted(predictions, key=lambda tup: tup[1],reverse=True)
	# output results
	count = 0
	fname = os.path.join(config['output_dir'], config['doc_files'][0]+'_autophrase.keywords')
	with open(fname, "w", encoding='utf-8') as fout:
		for pred in sorted_predictions:
			fout.write(pred[0]+'\n')
			count += 1
			if count>=config['number']:
				break


if __name__=='__main__':
	config_file = "../config/default.json"
	with open(config_file) as file:
		config = json.load(file)
	autophrase_extraction(config)