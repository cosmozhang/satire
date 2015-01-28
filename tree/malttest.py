## Cosmo Zhang @ Purdue 11/2014
## nlp project1
## Filename:malttest.py
## -*- coding: utf-8 -*-

import gc
import os
import codecs
import cPickle as cpcl
import sys
import string
import numpy
reload(sys)
import nltk
from nltk.parse.malt import MaltParser
from pprint import pprint
sys.setdefaultencoding("utf-8")

def get_file_list(dir_path):

    file_list = []
    for each in os.listdir(dir_path):
        if each.endswith(".txt"):
            file_list.append(each) 
    return file_list

def preprocess(s):
    s = s.decode('utf-8').replace(u'\u2013', '-').replace(u'\u201c', '"').replace(u'\u2019', '\'').replace(u'\u201d', '"').replace(u'\u2014', '-').replace(u'\u2026', '...').replace(u'\u2018', '\'').replace(u'\u200f', ' ')
    # print s
    return s.strip()

def mltprocess(tp, path, filenamels, docid):
    parser=MaltParser(working_dir='/home/cosmo/Dropbox/Purdue/nlp/maltparser-1.8/maltparser-1.8.jar', mco='engmalt.poly-1.7.mco', additional_java_args='-mx5000m')
    sdfdata = []
    for i in range(len(filenamels)):
        if (i+1)%100 == 0: print "%f%% of document %d of %s finished" % ((i+1)*100*1.0/len(filenamels), docid, tp) 
        filename = filenamels[i]
        h = open(path + filename, 'r')
        lines = h.readlines()
        h.close()
        headraw, bodyraw = preprocess(lines[0]), preprocess(lines[1])

        sentences = [headraw] + nltk.sent_tokenize(bodyraw)
        sdfparsed = [parser.raw_parse(sentence) for sentence in sentences]
        sdfdata.append(sdfparsed)
        # print sdfparsed
        # print sdfdata      
        # if i > 5: break
    return sdfdata


def main():
    dir_path = os.getcwd() + '/../rawdata/cnntxts/'
    cnnfilels = get_file_list(dir_path)

    partlen = (len(cnnfilels)-len(cnnfilels)%9)/9
    for i in range(10):
        if len(cnnfilels[i*partlen:]) >= partlen: partls = cnnfilels[i*partlen:(i+1)*partlen]
        elif len(cnnfilels[i*partlen:]) < partlen: partls = cnnfilels[i*partlen:]
        normalparsed = sdfprocess('normal', dir_path, partls, i)
        g = file('normalparse'+str(i)+'.data', 'wb')
        cpcl.dump(normalparsed, g) #
        g.close()
        del normalparse
        gc.collect()

    dir_path = os.getcwd() + '/../rawdata/oniontxts/'
    onionfilels = get_file_list(dir_path)
    partlen = (len(onionfilels)-len(onionfilels)%9)/9
    for i in range(10):
        if len(onionfilels[i*partlen:]) >= partlen: partls = onionfilels[i*partlen:(i+1)*partlen]
        elif len(onionfilels[i*partlen:]) < partlen: partls = onionfilels[i*partlen:]
        satireparsed = sdfprocess('satire', dir_path, partls, i)
        h = file('satireparse'+str(i)+'.data', 'wb')
        cpcl.dump(satireparsed, h)
        h.close()
        del satireparse
        gc.collect()

    print "Stanford Parser Process Done!"

if __name__ == "__main__":
    main()
