# Cosmo Zhang @ Purdue Jan/2015
# CS590 hw1
# Filename: wv_svm.py
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
import gensim, logging
import cPickle as cpcl
import sys
reload(sys)  
sys.setdefaultencoding('utf8')


class MySentences(object):
    def __init__(self, dt):
        self.dt = dt
        
    def __iter__(self):
            for docid in range(len(self.dt)):
                for qid in range(len(self.dt[docid][0])):
                    sinqs = [word_tokenize(sentence) for sentence in self.dt[docid][0][qid]]
                    for sid, sentence in enumerate(sinqs):
                        yield gensim.models.doc2vec.LabeledSentence(words=sentence, labels=['SENT_%s' % (str(docid) + '-' + str(qid) + '-' + str(sid)), "Doc_%s" % str(docid)])
                        

def main():

    f = open('data.dat', 'rb')
    data = cpcl.load(f)
    f.close()
    
    sentences = MySentences(data)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    model = gensim.models.Doc2Vec(alpha=0.025, min_alpha=0.025, workers=4, size=50, min_count=1)  # use fixed learning rate
    model.build_vocab(sentences)

    for epoch in range(10):
        model.train(sentences)
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay
    
    model.save('doc2vec_model')


if __name__ == "__main__":
    main()
