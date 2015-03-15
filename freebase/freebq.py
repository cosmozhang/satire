# Cosmo Zhang @ Purdue 12/2014
# nlp poject1
# Filename: freebq.py
# -*- coding: utf-8 -*-

import json
import urllib
import codecs
import cPickle as cpcl
import sys
import string
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


def preprocess(s):
    stupidpattern = r'[A-Z]*[, ]*[A-Z]{3,}\-'
    s = s.decode('utf-8').replace(u'\u2013', u'-').replace(u'\u201c', u'"').replace(u'\u2019', u'\'').replace(u'\u201d', u'"').replace(u'\u2014', u'-').replace(u'\u2026', u'...').replace(u'\u2018', u'\'').replace(u'\u200f', u' ').replace(u'\u200b', u'').replace(u'\xe2', u'-').replace(u'\xe9', u'e').replace(u'\xc2', u'A').replace(u'\xe0', u'a').replace(u'\xae', u'').replace(u'\xe7', u'c').replace(u'\xf1', u'n').replace(u'\xbd', u'1/2').replace(u'\xe1', u'a')
    toreplace = re.findall(stupidpattern, s)
    
    if toreplace != []:
        # print toreplace[0]
        s = s.replace(toreplace[0], '')
    # print s.strip()
    try:
        return s.strip().encode('ascii')
    except Exception, e:
        print e
        sys.exit('debug')

def sdfprocess(rawexpr):
    parser=NERTagger(path_to_model='/home/cosmo/Dropbox/Purdue/nlp/stanford-corenlp-full-2014-08-27/english.all.3class.distsim.crf.ser.gz', path_to_jar='/home/cosmo/Dropbox/Purdue/nlp/stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1.jar', java_options='-mx2000m')
    expr = preprocess(rawexpr)
    named_expr = rechunk(parser.tag(word_tokenize(expr)))
    for t in named_expr:
        if t[1] == 'PERSON':
            return t[0]
    return expr
    # print named_expr

def getpolideo(descr):
    democ, repub = 0, 0
    for word in word_tokenize(descr.lower()):
        # print word
        if (word == 'democratic') or (word == 'democracy') or (word == 'democrat'):
            democ += 1
        elif (word == 'republican') or (word == 'gop'):
            repub += 1
    if(democ == repub):
        ideo = 'Null'
    elif(democ > repub):
        ideo = 'democ'
    else:
        ideo = 'repub'
    return ideo
            


def main():
    api_key = open("api_key").read()
    service_url = 'https://www.googleapis.com/freebase/v1/search'

    f = open('qdata.dat', 'rb')
    data = cpcl.load(f)
    f.close()

    # g = open('testres.txt', 'w')
    # h = open('notfamous.txt', 'w')
    for idx in range(len(data)):
        each = data[idx]
        query = sdfprocess(each[0]) #1st element is the speaker
        # print query
        params = {'query': query, 'key': api_key, 'lang': "en", 'filter': '(any type:/people/person)', 'output': '(description /people/person/gender /people/person/age)'}
        #'filter': '(any type:/people/person)',
        url = service_url + '?' + urllib.urlencode(params)

        response = json.loads(urllib.urlopen(url).read())       
        if response['result'] != [] and response['result'][0]['score'] > 100:
            try:
                if response['result'][0]['output']['/people/person/age'] != {}:
                    age = response['result'][0]['output']['/people/person/age']['/people/person/age'][0]
                else:
                    age = 'Null'
                if response['result'][0]['output']['/people/person/gender'] != {}:
                    gender = response['result'][0]['output']['/people/person/gender']['/people/person/gender'][0]['name']
                else:
                    gender = 'Null'
                if response['result'][0]['output']['description'] != {}:
                    description = response['result'][0]['output']['description']['/common/topic/description'][0].replace('\n', '').encode('unicode-escape')
                else:
                    description = 'Null'
                if response['result'][0]['notable'] != {}:
                    notable = response['result'][0]['notable']['name']
                else:
                    notatle = 'Null'
            except:
                print "key error:\n", query, response['result'][0], '\n'
                sys.exit(1)
        else:
            # print 'bad', response
            age, gender, description, notable = 'Null', 'Null', 'Null', 'Null'
        # print response['result'][0]['notable']['name']
        
        polideo = getpolideo(description)
        print idx, age, gender, notable, polideo, '\n'

        
if __name__ == '__main__':
    main()
