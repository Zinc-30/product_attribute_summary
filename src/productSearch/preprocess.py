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

es = Elasticsearch("localhost:9200")
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
        if 'asin' in x:
            asin = x['asin']
        else:
            continue
        if 'feature' in x:
            for phrases in x[u'feature']:
                if len(phrases.split(" ")) > 5:
                    continue
        yield {"_index": "amazon","_type":"product", "_id": asin , "_source": x}

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
    helpers.bulk(es, actions=es_parse_product())

if __name__ == '__main__':
    main()
    print(es.search(index="amazon",doc_type="product",query={"match":{"iphone"}}))