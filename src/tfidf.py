import string
import os
import pke
import json
from pathlib import Path
import tqdm
from nltk.corpus import stopwords


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def tfidf(config, stoplist=list(string.punctuation)):
    path = Path(config['data_dir'])
    path_out = Path(config['output_dir'])
    num = config['number']
    extractor = pke.unsupervised.TfIdf()
    document_frequency = pke.load_document_frequency_file(path_out.joinpath('doc_freq.tsv.gz'))
    for file_name in tqdm.tqdm(config['doc_files']):
        # for file_name in tqdm.tqdm(path.glob('*.txt')):
        extractor.load_document(input=str(path.joinpath(file_name)), language='en', normalization=None)
        extractor.candidate_selection(n=3, stoplist=stoplist)
        extractor.candidate_weighting(document_frequency)
        keyphrases = extractor.get_n_best(num, redundancy_removal=True)
        mkdir(str(path_out.joinpath('/tfidf/')))
        with open(str(path_out.joinpath('/tfidf/')) + '/{}.json'.format(file_name), 'w') as file:
            json.dump({file_name: keyphrases}, file)


def caculate_freq(path, path_out, stoplist=list(string.punctuation)):
    pke.compute_document_frequency(path, path_out + '/doc_freq.tsv.gz', extension='txt', language='en',
                                   normalization=None,
                                   stoplist=stoplist, n=3)


if __name__ == '__main__':
    config_file = '../config/default.json'
    with open(config_file) as file:
        config = json.load(file)
    path = config['data_dir']
    path_out = config['output_dir']
    stoplist = list(string.punctuation)
    caculate_freq(path, path_out, stoplist)
    print('Using model: TFIDF')
    tfidf(config, stoplist)
    print('Finish model: TFIDF')
