# Cosmo Zhang @ Purdue 12/2014
# nlp poject1
# Filename: feature.py
# -*- coding: utf-8 -*-

import gc
import os
import codecs
import json
import urllib
import cPickle as cpcl
import sys
import string
import numpy
reload(sys)
import nltk
import re
#from nltk.tag.stanford import NERTagger
from nltk.tokenize import word_tokenize
from pprint import pprint
from progressbar import *
sys.setdefaultencoding("utf-8")


def freebasequery(data):
    api_key = open("api_key").read()
    service_url = 'https://www.googleapis.com/freebase/v1/search'

    for each in data:
        if each[1] = 'neg':
            label = 0
        elif each[1] = 'pos':
            label = 1
        
        query = element[0]
        params = {
            'query': query,
            'key': api_key
            }
        url = service_url + '?' + urllib.urlencode(params)
        response = json.loads(urllib.urlopen(url).read())
                    # print response
                    # '''
                    # g = open('testres.txt', 'w')
                    # g.write(response + '\n')
                    '''
                    for result in response:
                        for ele in result:
                            g.write(ele + '\n')
                    '''        
                    if response['result'] != [] and response['result'][0]['score'] < 100:
                        h.write(' '.join([part for part in element]) + '\n')
                        h.write('name: ' + response['result'][0]['name'] + '; notable: '+ response['result'][0]['notable']['name']+'\n')
                        h.write(each[0][each[1].index(sentence)].encode('utf-8')+'\n')
                        # print element, 'name: ' + response['result'][0]['name'] + '; notable: '+ response['result'][0]['notable']['name']
                        #print ' '.join([word[0] for word in sentence])
                        # print each[0]
                    # '''    
                    for result in response['result']:
                        # print result['name'].encode('unicode-escape') + ' (' + str(result['score']) + ')'

                        g.write(result['name'].encode('unicode-escape') + ' (' + str(result['score']) + ')\n')
                        if 'notable' in result:
                            # print 'notable: ' + result['notable']['name']
                            g.write('notable: ' + result['notable']['name'] + '\n')
    g.close()
    h.close()
        


def main():
    f = open('../annotated/data.dat', 'rb')
    data = cpcl.load(f)
    f.close



if __name__ == '__main__':
    main()
