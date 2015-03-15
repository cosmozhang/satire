# Cosmo Zhang @ Purdue 1/2015
# nlp poject1
# Filename: anno_data_format.py
# -*- coding: utf-8 -*-

import json
import cPickle as cpcl
import os
import string
import sys
import random
reload(sys)
sys.setdefaultencoding("utf-8")

def preprocess(s):
    s = s.decode('utf-8').replace(u'\u2013', '-').replace(u'\u201c', '"').replace(u'\u2019', "'").replace(u'\u201d', '"').replace(u'\u2014', '-').replace(u'\u2026', '...').replace(u'\u2018', "'").replace(u'\u200f', ' ').replace(u'\xa0', '').replace('\n', '')
    # print s
    #s.encode('ascii')
    try:
        return s
    except Exception, e:
        #print s#.encode('utf-8')
        print e
        sys.exit('debug')
    
        
def get_file_list(dir_path):

    file_list = []
    for each in os.listdir(dir_path):
        if each.endswith(".txt"):
            file_list.append(each) 
    return file_list

def getdata(data, filepath, category):
    h = open(filepath, 'r')
    lines = h.readlines()
    h.close()
    
    neweg = ''.join(lines[:-1])
    neweg = preprocess(neweg)
        
    
    data.append([[[neweg]], category])


def main():
    data = []
    anno_dir_path = '../annotated/neg/'
    cnnfilels = get_file_list(anno_dir_path)
    dir_path = os.getcwd() + '/cnntxts/'
    for f in cnnfilels:
        filepath = dir_path + f
        getdata(data, filepath, 'neg')

    anno_dir_path = '../annotated/pos/'
    onionfilels = get_file_list(anno_dir_path)
    dir_path = os.getcwd() + '/oniontxts/'
    for f in onionfilels:
        filepath = dir_path + f
        getdata(data, filepath, 'pos')

    # print len(data)
    random.shuffle(data)
    g = open('odata.dat', 'w')
    cpcl.dump(data, g)
    g.close()
    print 'Processing Done'


if __name__ == '__main__':
    main()
