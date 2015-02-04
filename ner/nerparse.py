## Cosmo Zhang @ Purdue 11/2014
## nlp project1
## Filename:nerparse.py
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
import re
from nltk.tag.stanford import NERTagger
from nltk.tokenize import word_tokenize
from pprint import pprint
from progressbar import *
sys.setdefaultencoding("utf-8")

def rechunk(ner_output):
    chunked, pos, prev_tag = [], "", None
    for i, word_pos in enumerate(ner_output):
        word, pos = word_pos
        if pos in ['PERSON', 'ORGANIZATION', 'LOCATION'] and pos == prev_tag:
            chunked[-1]+=word_pos
        else:
            chunked.append(word_pos)
        prev_tag = pos


    clean_chunked = [tuple([" ".join(wordpos[::2]), wordpos[-1]]) 
                    if len(wordpos)!=2 else wordpos for wordpos in chunked]

    return clean_chunked

def get_file_list(dir_path):

    file_list = []
    for each in os.listdir(dir_path):
        if each.endswith(".txt"):
            file_list.append(each) 
    return file_list

def preprocess(s):
    stupidpattern = r'[A-Z]*[, ]*[A-Z]{3,}\-'
    s = s.decode('utf-8').replace(u'\u2013', u'-').replace(u'\u201c', u'"').replace(u'\u2019', u'\'').replace(u'\u201d', u'"').replace(u'\u2014', u'-').replace(u'\u2026', u'...').replace(u'\u2018', u'\'').replace(u'\u200f', u' ').replace(u'\u200b', u'').replace(u'\xe2', u'-').replace(u'\xe9', u'e').replace(u'\xc2', u'A').replace(u'\xe0', u'a').replace(u'\xae', u'').replace(u'\xe7', u'c').replace(u'\xf1', u'n').replace(u'\xbd', u'1/2').replace(u'\xe1', u'a')
    toreplace = re.findall(stupidpattern, s)
    
    if toreplace != []:
        # print toreplace[0]
        s = s.replace(toreplace[0], '')
    # print s.strip()
    try:
        return s.strip().replace(u'(CNN) - ', u'').encode('ascii')
    except Exception, e:
        print e
        sys.exit('debug')

def sdfprocess(tp, path, filenamels):
    parser=NERTagger(path_to_model='/home/cosmo/Dropbox/Purdue/nlp/stanford-corenlp-full-2014-08-27/english.all.3class.distsim.crf.ser.gz', path_to_jar='/home/cosmo/Dropbox/Purdue/nlp/stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1.jar', java_options='-mx2000m')
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=len(filenamels)).start()
    sdfdata = []
    for idx in range(len(filenamels)):
        # if (i+1)%100 == 0: print "\n*****%f%% of documents of %s finished" % ((i+1)*100*1.0/len(filenamels), tp) 
        filename = filenamels[idx]
        h = open(path + filename, 'r')
        lines = h.readlines()
        h.close()
        headraw, bodyraw = preprocess(lines[0]), preprocess(lines[1])
        # print bodyraw
        bodysenls = [ele.decode('utf-8') for ele in nltk.sent_tokenize(bodyraw)]
        sentences = [headraw] + bodysenls
        sdfparsed = []
        for sentence in sentences:
            # print type(sentence)
            try:
                sdfparsed.append(rechunk(parser.tag(word_tokenize(sentence))))
            except:
                print filename
                sys.exit('debug')

        sdfdata.append((sentences, sdfparsed))
        # print sentences[0]
        # print sdfparsed
        pbar.update(idx + 1)
        # print sdfdata      
        # if i > 5: break
    return (sdfdata)


def main():
    #'''
    dir_path = os.getcwd() + '/../rawdata/cnntxts/'
    cnnfilels = get_file_list(dir_path)
    print "%d pieces of cnn news to parse" % len(cnnfilels)
    normalparsed = sdfprocess('normal', dir_path, cnnfilels)
    g = file('normalnerparse.data', 'wb')
    cpcl.dump(normalparsed, g) #
    g.close()
    del normalparsed
    gc.collect()
    #'''


    dir_path = os.getcwd() + '/../rawdata/oniontxts/'
    onionfilels = get_file_list(dir_path)
    print "%d pieces of onion news to parse" % len(onionfilels)
    satireparsed = sdfprocess('satire', dir_path, onionfilels)
    h = file('satireparse.data', 'wb')
    cpcl.dump(satireparsed, h)
    h.close()
    del satireparsed
    gc.collect()

    print "Stanford Parser Process Done!"

if __name__ == "__main__":
    main()
