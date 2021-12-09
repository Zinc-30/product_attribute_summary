import string
import pke
import json
from pathlib import Path
import tqdm
import shutil
import os
from nltk.corpus import stopwords

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def yake(config, stoplist):
    extractor = pke.unsupervised.YAKE()
    data_dir = Path(config['data_dir'])
    output_dir = Path(config['output_dir'])
    num = config['number']
    for file_name in tqdm.tqdm(config['doc_files']):
    #for file_name in tqdm.tqdm(path.glob('*.txt')):
        extractor.load_document(input=str(data_dir.joinpath(file_name)), language='en', normalization=None)
        extractor.candidate_selection(n=3, stoplist=stoplist)
        extractor.candidate_weighting(window=3, stoplist=stoplist)
        keyphrases = extractor.get_n_best(num, threshold=0.8, redundancy_removal=True)
        mkdir(str(output_dir.joinpath('yake/')))
        with open(str(output_dir) + '/{}_yake.keywords'.format(file_name), 'w') as file:
            for phrase in keyphrases:
                file.write(str(phrase[0]).lower() + '\n')

if __name__ == '__main__':
    config_file = '../config/default.json'
    with open(config_file) as file:
        config = json.load(file)
    path = config['data_dir']
    path_out = config['output_dir']
    print('Using model: YAKE')
    stoplist = stopwords.words('english')
    yake(config, stoplist)
    print('Finish model: YAKE')