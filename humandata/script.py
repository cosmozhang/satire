##Cosmo Zhang @ Purdue 2015/2
##Filename: script.py
##for analysis of human annotated data
# -*- coding: utf-8 -*-

import sys
import csv



def main():
    filename = sys.argv[1]
    f = open(filename, 'r')
    hdata = csv.reader(f, delimiter=',', quotechar='"')
    # f.close()

    res = {'hit':0, 'miss':0, 'fa':0, 'cr':0}
    
    for nline in hdata:
        #nline = line.split(',')
        # print nline[7], nline[13]
        if 'real' in nline[7] and nline[13] == '1':
            res['miss'] += 1
        elif 'satirical' in nline[7] and nline[13] == '1':
            res['hit'] += 1
        elif 'real' in nline[7] and nline[13] == '0':
            res['cr'] += 1
        elif 'satirical' in nline[7] and nline[13] == '0':
            res['fa'] += 1
        else:
            pass
    
    sumcount = res['hit'] + res['miss'] + res['fa'] + res['cr']
    predP = res['hit'] + res['fa']
    trueP = res['hit'] + res['miss']
    print 'accuracy: %0.2f%%' % ((res['hit'] + res['cr'])*100.0/sumcount)
    print 'precision: %0.2f%%' % (res['hit']*100.0/predP)
    print 'recall: %0.2f%%' % (res['hit']*100.0/trueP)
    print 'F-score: %0.2f%%' % (2*(res['hit']*100.0/predP)*(res['hit']*1.0/trueP)/((res['hit']*1.0/predP)+(res['hit']*1.0/trueP)))
    f.close()





if __name__ == "__main__":
    main()







