import pke
import tqdm
from pathlib import Path
import os
import json



def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def TopicRank(config):
    doc_files = config['doc_files']
    path = Path(config['data_dir'])
    path_out = Path(config['output_dir'])
    num = config['number']
    extractor = pke.unsupervised.TopicRank()
    for file_name in tqdm.tqdm(doc_files):
        extractor.load_document(input=str(path.joinpath(file_name)), language='en')
        extractor.candidate_selection()
        extractor.candidate_weighting()
        keyphrases = extractor.get_n_best(n=num)
        mkdir(str(path_out.joinpath('topicrank/')))
        with open(str(path_out.joinpath('topicrank/')) + '/{}.keywords'.format(file_name), 'w') as file:
            json.dump({file_name: keyphrases}, file)
    

if __name__ == '__main__':
    config_file = '../config/default.json'
    with open(config_file) as file:
        config = json.load(file)
    path = config['data_dir']
    path_out = config['output_dir']
    print('Using model: TopicRank')
    TopicRank(config)
    print('Finish model: TopicRank')