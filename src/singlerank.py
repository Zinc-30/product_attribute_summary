import pke
import tqdm
from pathlib import Path
import json




def SingleRank(config, pos = {'NOUN', 'PROPN', 'ADJ'}, window=10):
    doc_files = config['doc_files']
    path = Path(config['data_dir'])
    path_out = Path(config['output_dir'])
    num = config['number']
    for file_name in tqdm.tqdm(doc_files):
        extractor = pke.unsupervised.SingleRank()
        extractor.load_document(input=str(path.joinpath(file_name)), language='en', normalization=None)
        extractor.candidate_selection(pos=pos)
        extractor.candidate_weighting(window=window, pos=pos)
        keyphrases = extractor.get_n_best(n=num)
        with open(str(path_out) + '/{}_singlerank.keywords'.format(file_name), 'w') as file:
            json.dump({file_name: keyphrases}, file)
    

if __name__ == '__main__':
    config_file = '../config/default.json'
    with open(config_file) as file:
        config = json.load(file)
    path = config['data_dir']
    path_out = config['output_dir']
    print('Using model: SingleRank')
    SingleRank(config)
    print('Finish model: SingleRank')