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
# import scipy
import sys
# from hw1 import *
import gensim, logging
from nltk.corpus import movie_reviews
reload(sys)  
# sys.setdefaultencoding('utf8')


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
        
    def __iter__(self):
        for category in ['pos', 'neg']:
            for fname in os.listdir(self.dirname + category):
                if fname.endswith('.txt'):
                    # try:
                    egwords = [word_tokenize(sentence) for sentence in sent_tokenize(codecs.open(os.path.join(self.dirname, category, fname), 'r', 'latin2').read().decode('utf-8'))]
                    # except:
                        # print os.path.join(self.dirname, category, fname)
                    for sid, sentence in enumerate(egwords):
                        # print uid
                        # print (category + '-' + fname)
                        yield gensim.models.doc2vec.LabeledSentence(words=sentence, labels=['SENT_%s' % (category + '-' + fname + '-' + str(sid)), 'Doc_%s' % (category + '-' + fname)])
                        

def main():
    #read data
    # dataset, allwords = getdataset()
    # print dataset[0][1]
    parent_dir_path = '/home/cosmo/Dropbox/Purdue/CS590/hws/hw1/tokens/'
    sentences = MySentences(parent_dir_path)
    # sentences = [gensim.models.doc2vec.LabeledSentence(words=[u'some', u'words', u'here'], labels=[u'SENT_1']), gensim.models.doc2vec.LabeledSentence(words=[u'give', u'a', u'shot'], labels=[u'SENT_2'])]
    # print sentences
    # print type(sentences)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    
    # pass
    model = gensim.models.Doc2Vec(alpha=0.025, min_alpha=0.025)  # use fixed learning rate
    model.build_vocab(sentences)

    for epoch in range(10):
        model.train(sentences)
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay
    
    model.save('doc2vec_model')


if __name__ == "__main__":
    main()
