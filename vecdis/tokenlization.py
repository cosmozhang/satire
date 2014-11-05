#cosmo zhang @ Purdue 2014/10
#filename: tokenlization.py
#nlp svm binary features
# -*- coding: utf-8 -*-

import nltk
import string
import os
import sys

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

def tokenize(tp, path, filename, head):
    # print filename
    #removal = string.whitespace + string.punctuation + string.digits
    h = open(path + filename, 'r')
    # tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
    lines = h.readlines()
    h.close()
    
    headraw = preprocess(lines[0])
    bodyraw = preprocess(lines[1])
    # print headraw.lower()
    # print bodyraw.lower()
    headdoc = nltk.word_tokenize(headraw.lower())
    bodydoc = nltk.word_tokenize(bodyraw.lower())
    
    if head == True:
        # print headdoc
        g = open(os.getcwd() + '/./tokened_head/' + tp + '/' + filename, 'w')
        doc = headdoc
    elif head == False:
        g = open(os.getcwd() + '/./tokened/' + tp + '/' + filename, 'w')
        doc = headdoc + bodydoc
    # print filename
    # print doc
    for word in doc:
        # print word
        # g.write(word + '\n')
        g.write(word.encode('utf-8') + '\n')
    g.close()

def main():
    # print os.getcwd() + "\n"
    head = False
    for arg in sys.argv:
        if arg == "Head" or arg == "-H":
            head = True
    if head == True: 
        print "Tokenize just head"
    elif head == False:
        print "Tokenize the whole document"
    dir_path = os.getcwd() + '/../rawdata/cnntxts/'
    cnnfilels = get_file_list(dir_path)
    for f in cnnfilels:
        tokenize('normal', dir_path, f, head)


    dir_path = os.getcwd() + '/../rawdata/oniontxts/'
    onionfilels = get_file_list(dir_path)
    for f in onionfilels:
        tokenize('satire', dir_path, f, head)
        
    print "******\nDocuments tokenlized\n******"


if __name__ == '__main__':
    main()

