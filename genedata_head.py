#cosmo zhang @ Purdue 2014/10
#filename: genedata.py
#nlp svm binary features
# -*- coding: utf-8 -*-

import nltk
import string

def getegvec(tp, fnm, wdic):
    removal = string.whitespace + string.punctuation + string.digits
    h = open ('./satire/' + tp + '/' +fnm, 'r')
    tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
    doc = tokenizer.tokenize(h.readline().lower())
    fvec = {}
    #print doc
    for word in doc:
        if word.strip(removal) != '':
            if word not in wdic: #global dic
                wdic[word] = {'index':len(wdic)+1, 'num':1}
            else:
                wdic[word]['num'] += 1
            fvec[wdic[word]['index']] = 1
    #print fvec
    fvecls = sorted(fvec.items(), key = lambda x: x[0], reverse = False)
    #print fvec
    '''
    tmls = []
    for item in fvec:
        print item
        tmls.append(str(item[0]) + ':' str(item[1]))
    '''    
    fvect = [str(x[0]) + ':' + str(x[1]) for x in fvecls]
    #print fvec
    strfvec = ' '.join(fvect)
    h.close()
    return (wdic, strfvec)


def dealdt(tp, hgdic):
    quefname = './satire/' + tp + '-class'
    egdt = open(quefname, 'r').readlines()
    
    dt = []
    print len(egdt)
    for eginfo in egdt:
        eginfo = eginfo.strip('\n').split()
        #print eginfo
        filename = eginfo[0]
        tg = eginfo[1]
        hgdic, egvec = getegvec(tp, filename, hgdic)
        if tg == "true":
            label = "-1 "
        elif tg == "satire":
            label = "+1 "
        dt.append(label + ''.join(egvec))
        
    return (dt, hgdic)

def main():
    
    hgdic = {}
    train_data, hgdic = dealdt('training', hgdic)
    test_data, hgdic = dealdt('test', hgdic)
    
    f = open('traindtsvm_head.csv', 'w')
    g = open('testdtsvm_head.csv', 'w')
    for line in train_data:
        f.write(line + '\n')
    for line in test_data:
        #for element in line:
        g.write(line + '\n')
    print len(train_data)
    print len(test_data)
    f.close()
    g.close()


if __name__ == '__main__':
    main()

