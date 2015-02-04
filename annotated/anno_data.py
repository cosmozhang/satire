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


def preprocess(s):
    s = s.decode('utf-8').replace(u'\u2013', '-').replace(u'\u201c', '"').replace(u'\u2019', "'").replace(u'\u201d', '"').replace(u'\u2014', '-').replace(u'\u2026', '...').replace(u'\u2018', "'").replace(u'\u200f', ' ').replace(u'\xa0', '').replace('\n', '')
    # print s
    #s.encode('ascii')
    try:
        return s.encode('ascii')
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
    
    neweg = []
    for line in lines[1:-1]:
        line = preprocess(line)
        newline = [each.strip('"') for each in line.split(' "')]
        
        neweg.append(newline)
    data.append([neweg, category])


def main():
    data = []
    dir_path = os.getcwd() + '/cnntxts/'
    cnnfilels = get_file_list(dir_path)
    for f in cnnfilels:
        filepath = dir_path + f
        getdata(data, filepath, 'neg')

    dir_path = os.getcwd() + '/oniontxts/'
    onionfilels = get_file_list(dir_path)
    for f in onionfilels:
        filepath = dir_path + f
        getdata(data, filepath, 'pos')

    # print len(data)
    random.shuffle(data)
    g = open('data.dat', 'w')
    cpcl.dump(data, g)
    g.close()


if __name__ == '__main__':
    main()
