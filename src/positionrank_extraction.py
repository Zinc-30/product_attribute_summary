import pke
import os
import json

def positionrank_extract(config):
    # define the valid Part-of-Speeches to occur in the graph
    pos = {'NOUN', 'PROPN', 'ADJ'}
    # define the grammar for selecting the keyphrase candidates
    grammar = "NP: {<ADJ>*<NOUN|PROPN>+}"

    extractor = pke.unsupervised.PositionRank()


    infile = os.path.join(config['data_dir'],config['doc_files'][0])
    outfile = os.path.join(config['output_dir'],config['doc_files'][0]+'_posrank.keywords')
    print(outfile)

    # 2. load the content of the document.
    extractor.load_document(input=infile,
                            language='en',
                            normalization=None)

    # 3. select the noun phrases up to 3 words as keyphrase candidates.
    extractor.candidate_selection(grammar=grammar,
                                  maximum_word_number=3)

    # 4. weight the candidates using the sum of their word's scores that are
    #    computed using random walk biaised with the position of the words
    #    in the document. In the graph, nodes are words (nouns and
    #    adjectives only) that are connected if they occur in a window of
    #    10 words.
    extractor.candidate_weighting(window=10,
                                  pos=pos)

    # 5. get the 10-highest scored candidates as keyphrases
    keyphrases = extractor.get_n_best(n=config['number'])
    print(keyphrases)
    with open(outfile, "w", encoding='utf-8') as fout:
        for kp in keyphrases:
            fout.write(kp[0]+'\n')

if __name__ == '__main__':
    config_file = "../config/default.json"
    with open(config_file) as file:
        config = json.load(file)
    positionrank_extract(config)
