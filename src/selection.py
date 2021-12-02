#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-11-30 21:41
# @Author  : hxinaa

from transformers import BertTokenizer, BertModel
import torch.nn.functional as F
import torch

import random

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained("bert-base-multilingual-cased")

def get_cls_emb(text1):
    encoded_text1 = tokenizer(text1,padding=True, truncation=True, return_tensors='pt')
    return model(**encoded_text1)[0][:,0]

def similarity_bert(text1,text2):
    cls_emb1 = get_cls_emb(text1)
    cls_emb2 = get_cls_emb(text2)
    return F.cosine_similarity(cls_emb1,cls_emb2).item()

def need_merge(phrase,cluster,theta):
    for phrase_other in cluster:
        if similarity_bert(phrase,phrase_other) < theta:
            return False
    return True


def cluster_phrases(phrases,theta):
    candidates = phrases
    selected = []
    for p1 in candidates:
        merge = False
        for cluster in selected:
            if need_merge(p1,cluster,theta):
                merge = True
                cluster.append(p1)
                break
        if not merge:
            selected.append([p1])
    return selected

def selected_represent_phrase(clusters,rand):
    ans = []
    for c in clusters:
        if rand:
            rand_idx = random.randint(0, len(c) - 1)
            ans.append(c[rand_idx])
        else:
            embs = torch.stack([get_cls_emb(p) for p in c], dim=0)
            centroid = torch.mean(embs, dim=0)
            similarities = F.cosine_similarity(embs, centroid.unsqueeze(0).expand(embs.size()),2)
            idx = torch.topk(similarities, k=1).indices[0].item()
            ans.append([c[idx]])
    return ans

def selection(phrase_list):
    clusters = cluster_phrases(phrase_list,0.6)
    # print(clusters)
    pruned_list = selected_represent_phrase(clusters,False)
    return pruned_list


if __name__ == '__main__':
    phrase_list = ["hello word","test data","computer game","west wood","greet game","good video games"]
    print(selection(phrase_list))
