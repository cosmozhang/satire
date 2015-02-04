#cosmo zhang @ Purdue 2014/10
#filename: genedata.py
#nlp svm binary features
# -*- coding: utf-8 -*-

import nltk
import string
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

def getfref(odt, ils):
    ndt = [[] for x in range(len(ils)-1)]
    wdic = {} #global dic
    for idx in range(len(ils)-1):
        for i in range(ils[idx], ils[idx+1]):
            fvec = {}
            # print i
            for eachquote in odt[i][0]:
                for sent in eachquote:
                    for word in word_tokenize(sent):
                        if word not in wdic: #global dic
                            wdic[word] = {'index':len(wdic)+1, 'num':1}
                        else:
                            wdic[word]['num'] += 1
                        if wdic[word]['index'] not in fvec: #local dic
                            fvec[wdic[word]['index']] = 1
                        else:
                            fvec[wdic[word]['index']] += 1
            fvecls = sorted(fvec.items(), key = lambda x: x[0], reverse = False)
            fvect = [str(x[0]) + ':' + str(x[1]) for x in fvecls]
            if odt[i][1] == "neg":
                label = "-1 "
            elif odt[i][1] == "pos":
                label = "+1 "
            ndt[idx].append(label + ''.join(' '.join(fvect)))
    return ndt

def getbinf(odt, ils):
    ndt = [[] for x in range(len(ils)-1)]
    wdic = {}
    for idx in range(len(ils)-1):
        for i in range(ils[idx], ils[idx+1]):
            fvec = {}
            # print i
            for eachquote in odt[i][0]:
                for sent in eachquote:
                    for word in word_tokenize(sent):
                        if word not in wdic: #global dic
                            wdic[word] = {'index':len(wdic)+1, 'num':1}
                        else:
                            wdic[word]['num'] += 1
                        fvec[wdic[word]['index']] = 1
            fvecls = sorted(fvec.items(), key = lambda x: x[0], reverse = False)
            fvect = [str(x[0]) + ':' + str(x[1]) for x in fvecls]
            if odt[i][1] == "neg":
                label = "-1 "
            elif odt[i][1] == "pos":
                label = "+1 "
            ndt[idx].append(label + ''.join(' '.join(fvect)))
    return ndt

def main():
    print sys.argv[1:]
    if ('-B' in sys.argv[1:]) or ('binary' in sys.argv[1:]):
        ftype = "binary"
    elif ('-F' in sys.argv[1:]) or ('frequency' in sys.argv[1:]):
        ftype = "frequency"
    else:
        print 'format: python %s [-B/-F]' % sys.argv[0]  
        sys.exit(1)
    f = open('../annotated/data.dat', 'rb')
    data = cpcl.load(f)
    f.close
    datalen = len(data)    
    sublen = int(datalen/5.0)
    indls = [0, sublen, 2*sublen, 3*sublen, 4*sublen, datalen]

    if ftype == 'binary':
        print "generate binary features"
        dataset = getbinf(data, indls)

    if ftype == 'frequency':
        print "generate frequency features"
        dataset = getfref(data, indls)


    idset = [(0, 1, 2, 3, 4), (1, 2, 3, 4, 0), (2, 3, 4, 0, 1), (3, 4, 0, 1, 2), (4, 0, 1, 2, 3)]
    for (i, j, k, m, n) in idset:
        f = open(ftype + '_train_dataset4svm_' + str(i) + '.csv', 'w')
        for line in (dataset[j] + dataset[k] + dataset[m] + dataset[n]):
            f.write(line + '\n')
        f.close()
        
        g = open(ftype + '_test_dataset4svm_' + str(i) + '.csv', 'w')
        for line in (dataset[i]):
            g.write(line + '\n')
        g.close()

    

if __name__ == '__main__':
    main()

