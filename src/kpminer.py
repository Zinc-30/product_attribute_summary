import string
import pke
import os
import shutil
import json
from pathlib import Path
import tqdm
from nltk.corpus import stopwords

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def kpminer(config, stoplist=list(string.punctuation)):
    path = Path(config['data_dir'])
    path_out = Path(config['output_dir'])
    num = config['number']
    extractor = pke.unsupervised.KPMiner()
    document_frequency = pke.load_document_frequency_file(str(path_out.joinpath('kpminer_source/doc_freq.tsv.gz')))
    for file_name in tqdm.tqdm(config['doc_files']):
    #for file_name in tqdm.tqdm(path.glob('*.txt')):
        extractor.load_document(input=str(path.joinpath(file_name)), language='en', normalization=None)
        extractor.candidate_selection(lasf=3, cutoff=400, stoplist=stoplist)
        extractor.candidate_weighting(df=document_frequency, alpha=2.3, sigma=3.0)
        keyphrases = extractor.get_n_best(num, redundancy_removal=True)
        mkdir(str(path_out.joinpath('kpminer/')))
        with open(str(path_out.joinpath('kpminer/')) + '/{}.keywords'.format(file_name), 'w') as file:
            for phrase in keyphrases:
                file.write(str(phrase) + '\n')
    shutil.rmtree(path_out.joinpath('kpminer_source/'))

def caculate_freq(config, stoplist=list(string.punctuation)):
    data_dir = Path(config['data_dir'])
    output_dir = Path(config['output_dir'])
    input_total = output_dir.joinpath('kpminer_source/')
    out_freq= input_total.joinpath('doc_freq.tsv.gz')
    mkdir(str(input_total))
    for file_name in config['doc_files']:
        shutil.copy(data_dir.joinpath(file_name), input_total)
    pke.compute_document_frequency(str(input_total), str(out_freq), extension='txt',
                                   language='en',
                                   normalization=None,
                                   max_length=5100000,
                                   stoplist=stoplist, n=3)


if __name__ == '__main__':
    config_file = '../config/default.json'
    with open(config_file) as file:
        config = json.load(file)
    path = config['data_dir']
    path_out = config['output_dir']
    stoplist = list(string.punctuation)
    caculate_freq(config, stoplist)
    print('Using model: KPMINER')
    kpminer(config, stoplist)
    print('Finish model: KPMINER')

