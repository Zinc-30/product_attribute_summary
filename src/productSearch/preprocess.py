#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-12-14 15:12
# @Author  : hxinaa
from sys import argv
import logging
import time
import json
import gzip
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import copy

es = Elasticsearch("localhost:9201")
product_file = "../../data/All_Amazon_Meta.json.gz"
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('time cost {:.2f} second'.format(time.time() - start))
        return res
    return wrapper

def es_parse_product():
    for l in gzip.open(product_file, 'r'):
        x = json.loads(l)
        cleanx = {}
        if 'asin' in x:
            asin = x['asin']
            cleanx['asin'] = asin
        else:
            continue
        if 'feature' in x:
            cleanx['feature'] = []
            for phrases in x[u'feature']:
                if len(phrases.split(" ")) > 5:
                    continue
                cleanx['feature'].append(phrases)
        if 'details' in x:
            cleanx['details'] = {}
            for k in x['details']:
                newk = k.strip().replace('.','_')
                if len(newk)>0:
                    cleanx['details'][newk] = x['details'][k]
        if 'title' in x:
            cleanx['title'] = x['title'].strip()
        if 'main_cat' in x:
            cleanx['main_cat'] = x['main_cat']
        if 'price' in x and len(x['price'])>0:
            cleanx['price'] = x['price']
        if 'brand' in x and len(x['brand'])>0:
            cleanx['brand'] = x['brand']
        if 'category' in x:
            cleanx['category'] = copy.deepcopy(x['category'])
        if 'description' in x:
            cleanx['description'] = copy.deepcopy(x['description'])
        yield {"_index": "amazon","_type":"product", "_id": asin , "_source": cleanx}

def es_parse_review(review_file):
    for l in gzip.open(review_file, 'r'):
        x = json.loads(l)
        if 'asin' in x:
            asin = x['asin']
        else:
            continue
        yield {"_index": "amazon", "_type": "review", "_source": x}

def es_generator():
    for x in range(10):
        yield {"_index": "test","_type":"_doc", "_source": {"value": x}}
@timer
def main():
    helpers.bdulk(es, actions=es_parse_product())


def get_prodcut_info_by_id(pid):
    body = {'match': {'asin': pid}}
    res = es.search(index="amazon", query=body)
    ans = [x['_source'] for x in res['hits']['hits']][0]
    return ans

def domain_review():
    """
    generate a domain review set
    select the reviews for the items in domain based on asin
    :param reviewfile: the .gz file to extract reviews
    :param domain: the product domain to extract
    :return: a list of reviews
    """

    body = {'match': {'description': "Laptop keyboard"} and {'title': "keyboard"} and {"main_cat":"Computers"}}
    res = es.search(index="amazon", query=body, size=1000)
    keyboard_ids = [x['_source']['asin'] for x in res['hits']['hits']]
    print(keyboard_ids)

    body = {'match': {'description': "GB"} and {'title': "computer"} and {"main_cat": "Computers"} and {"brand":"apple lenovo HP Acer dell asus"}}
    res = es.search(index="amazon", query=body, size=1000)
    computer_ids = [x['_source']['asin'] for x in res['hits']['hits']]
    print(computer_ids)
    with open('../../data/keyboard_ids.txt','w') as f:
        for id in keyboard_ids:
            f.write(id+'\n')
    with open('../../data/computer_ids.txt','w') as f:
        for id in computer_ids:
            f.write(id+'\n')







if __name__ == '__main__':
    info = get_prodcut_info_by_id('B00WWIGLWY')
    print(info)
    domain_review()