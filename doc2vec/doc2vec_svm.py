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
# import scipy
import sys
# from hw1 import *
import gensim, logging
from nltk.corpus import movie_reviews
reload(sys)  
# sys.setdefaultencoding('utf8')

def get_file_list(dir_path):

    file_list = []
    for each in os.listdir(dir_path):
        if each.endswith(".txt"):
            file_list.append(each) 
    return file_list

def main():
    model = gensim.models.Doc2Vec.load('doc2vec_model')
    dataset = [[], [], []]
    categories = ['pos', 'neg']
    parent_dir_path = '/home/cosmo/Dropbox/Purdue/CS590/hws/hw1/tokens/'
    endidxs = [0, 233, 466, 699]
    # print len(dataset)
    
    for idx in range(3):
        filerange = range(endidxs[idx], endidxs[idx+1])
        for category in categories:
            for fileid in get_file_list(parent_dir_path + category):
                if int(fileid[2:5]) in filerange:
                    docvec = model['Doc_%s' % (category + '-' + fileid)]
                    
                    egfvec = [str(ind+1) + ':' + str(value) for ind, value in enumerate(docvec)]

                    if category == "neg":
                        label = "-1 "
                    elif category == "pos":
                        label = "+1 "
                    dataset[idx].append(label + ''.join(' '.join(egfvec)))
        random.shuffle(dataset[idx])

    idset = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    for (i, j, k) in idset:
        f = open('train_dataset4svm_' + str(i) + '.csv', 'w')
        for line in (dataset[j] + dataset[k]):
            f.write(line + '\n')
        f.close()
        
        g = open('test_dataset4svm_' + str(i) + '.csv', 'w')
        for line in (dataset[i]):
            g.write(line + '\n')
        g.close()


if __name__ == '__main__':
    main()


