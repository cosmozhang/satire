# Cosmo Zhang @ Purdue Jan/2015
# CS590 hw1
# Filename: doc2vec_svm.py
# -*- coding: utf-8 -*-

import nltk
import random
import os
import sys
from nltk import word_tokenize
from nltk import sent_tokenize
import pprint
import codecs
from nltk import metrics
import collections
from nltk.corpus import stopwords
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.probability import FreqDist, ConditionalFreqDist
import sys
import cPickle as cpcl
import gensim, logging
reload(sys)  
sys.setdefaultencoding('utf8')

def main():
    model = gensim.models.Doc2Vec.load('doc2vec_model')
    f = open('data.dat', 'rb')
    data = cpcl.load(f)
    f.close
    datalen = len(data)    
    sublen = int(datalen/5.0)
    indls = [0, sublen, 2*sublen, 3*sublen, 4*sublen, datalen]
    dataset = [[] for x in range(len(indls)-1)]

    
    for idx in range(len(indls)-1):
        for docid in range(indls[idx], indls[idx+1]):
            docvec = model["Doc_%s" % str(docid)]
            doc = data[docid]        
            egfvec = [str(ind+1) + ':' + str(value) for ind, value in enumerate(docvec)]
            if data[docid][1] == "neg":
                label = "-1 "
            elif data[docid][1] == "pos":
                label = "+1 "
            dataset[idx].append(label + ''.join(' '.join(egfvec)))
        random.shuffle(dataset[idx])

    idset = [(0, 1, 2, 3, 4), (1, 2, 3, 4, 0), (2, 3, 4, 0, 1), (3, 4, 0, 1, 2), (4, 0, 1, 2, 3)]
    for (i, j, k, m, n) in idset:
        f = open('train_dataset4svm_' + str(i) + '.csv', 'w')
        for line in (dataset[j] + dataset[k] + dataset[m] + dataset[n]):
            f.write(line + '\n')
        f.close()
        
        g = open('test_dataset4svm_' + str(i) + '.csv', 'w')
        for line in (dataset[i]):
            g.write(line + '\n')
        g.close()


if __name__ == '__main__':
    main()


