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

def name_title(data):
    parser=NERTagger(path_to_model='/home/cosmo/Dropbox/Purdue/nlp/stanford-corenlp-full-2014-08-27/english.all.3class.distsim.crf.ser.gz', path_to_jar='/home/cosmo/Dropbox/Purdue/nlp/stanford-corenlp-full-2014-08-27/stanford-corenlp-3.4.1.jar', java_options='-mx2000m')
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=len(filenamels)).start()
    
    for idx in range(len(data)):
        for qidx in range(len(data[idx][0])):
            part = data[idx][0][qidx]
            name = rechunk(parser.tag(word_tokenize(part)))
            if name != None:
                title = part.replace(name, '')
            else:
                title = part
            data[idx][0][qidx] = [title, name]
        
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











def freebasequery():
    api_key = open("api_key").read()
    service_url = 'https://www.googleapis.com/freebase/v1/search'

    f = open('data.dat', 'rb')
    satiredata = cpcl.load(f)
    f.close()

    g = open('testres.txt', 'w')
    h = open('notfamous.txt', 'w')
    for each in satiredata:
        # print each[0]
        g.write('\tdocument level\n')
        for sentence in each[1]:
            g.write('\t\tsentence level\n')
            for element in sentence:
                if element[1] == 'PERSON' or element[1] == 'ORGANIZATION':
                    # print element
                    g.write('\t\t\tentity level:' + element[0] + ', ' + element[1]+ '\n')
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
    




if __name__ == '__main__':
    main()
