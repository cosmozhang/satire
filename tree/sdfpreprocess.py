## Cosmo Zhang @ Purdue 11/2014
## nlp project1
## Filename:sdfpreprocess.py
## -*- coding: utf-8 -*-

import os
import codecs
import cPickle as cpcl
import sys
import string
import numpy
reload(sys)
import nltk
from nltk.parse.stanford import StanfordParser
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

def sdfprocess(tp, path, filenamels):
    parser=StanfordParser(path_to_jar='/home/cosmo/Dropbox/Purdue/nlp/stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1.jar', path_to_models_jar='/home/cosmo/Dropbox/Purdue/nlp/stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1-models.jar', model_path='edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz', java_options='-mx5000m')
    sdfdata = []
    for i in range(len(filenamels)):
        if (i+1)%100 == 0: print "%f%% of %s finished" % ((i+1)*100*1.0/len(cnnfilels), tp) 
        filename = filenamels[i]
        h = open(path + filename, 'r')
        lines = h.readlines()
        h.close()
        headraw, bodyraw = preprocess(lines[0]), preprocess(lines[1])

        sentences = [headraw] + nltk.sent_tokenize(bodyraw)
        sdfparsed = parser.raw_parse_sents(sentences)
        sdfdata.append(sdfparsed)
        # print sdfparsed
        # print sdfdata      
        # if i > 5: break
    return sdfdata


def main():
    dir_path = os.getcwd() + '/../rawdata/cnntxts/'
    cnnfilels = get_file_list(dir_path)
    normalparsed = sdfprocess('normal', dir_path, cnnfilels)
    g = file('normalparse.data', 'wb')
    cpcl.dump(normalparsed, g) #
    g.close()

    dir_path = os.getcwd() + '/../rawdata/oniontxts/'
    onionfilels = get_file_list(dir_path)
    satireparsed = sdfprocess('satire', dir_path, onionfilels)
    h = file('satireparse.data', 'wb')
    cpcl.dump(satireparsed, h)
    h.close()
    print "Stanford Parser Process Done!"

if __name__ == "__main__":
    main()
