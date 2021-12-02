import string
import os
import shutil
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
    document_frequency = pke.load_document_frequency_file(str(path_out.joinpath('tfidf_source/doc_freq.tsv.gz')))
    for file_name in tqdm.tqdm(config['doc_files']):
        # for file_name in tqdm.tqdm(path.glob('*.txt')):
        extractor.load_document(input=str(path.joinpath(file_name)), language='en', normalization=None)
        extractor.candidate_selection(n=3, stoplist=stoplist)
        extractor.candidate_weighting(document_frequency)
        keyphrases = extractor.get_n_best(num, redundancy_removal=True)
        mkdir(str(path_out.joinpath('tfidf/')))
        with open(str(path_out) + '/{}_tfidf.keywords'.format(file_name), 'w') as file:
            for phrase in keyphrases:
                file.write(str(phrase) + '\n')
    shutil.rmtree(path_out.joinpath('tfidf_source/'))

def caculate_freq(config, stoplist=list(string.punctuation)):
    data_dir = Path(config['data_dir'])
    output_dir = Path(config['output_dir'])
    input_total = output_dir.joinpath('tfidf_source/')
    out_freq = input_total.joinpath('doc_freq.tsv.gz')
    mkdir(str(input_total))
    for file_name in config['doc_files']:
        shutil.copy(data_dir.joinpath(file_name), input_total)
    pke.compute_document_frequency(str(input_total), str(out_freq), extension='txt',
                                   language='en',
                                   normalization=None,
                                   stoplist=stoplist,
                                   max_length=5100000,
                                   n=3)


if __name__ == '__main__':
    config_file = '../config/default.json'
    with open(config_file) as file:
        config = json.load(file)
    path = config['data_dir']
    path_out = config['output_dir']
    stoplist = list(string.punctuation)
    caculate_freq(config, stoplist)
    print('Using model: TFIDF')
    tfidf(config, stoplist)
    print('Finish model: TFIDF')
