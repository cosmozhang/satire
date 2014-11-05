#cosmo zhang @ Purdue 2014/11
#filename: variance.py
#variance of vectors
# -*- coding: utf-8 -*-

import numpy as np
from numpy import linalg as LA
import os
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys

def vecsamplevar(ls):
    vecs = np.array(ls)
    mean = np.mean(vecs, axis = 0)
    disls = []
    for vec in ls:
        disls.append(LA.norm(np.subtract(vec, mean), 2))

    avgdis = sum(disls)*1.0/(len(disls))
    return avgdis

def docprocess(path, filename):
    f = open(path + filename, 'r')
    data = f.readlines()
    f.close()
    vcs = []
    # print data[1].split(', ')
    for line in data:
        vec = [float(x) for x in line.split(', ')]
        vcs.append(vec)
    avgdis = vecsamplevar(vcs)
    return avgdis


def get_file_list(dir_path):

    file_list = []
    for each in os.listdir(dir_path):
        if each.endswith(".txt"):
            file_list.append(each) 
    return file_list


def plotting(ls1, ls2, head):
    # print ls1, ls2
    mu1 = np.mean(ls1)
    mu2 = np.mean(ls2)
    sigma1 = np.std(ls1) # standard deviation of distribution
    sigma2 = np.std(ls2)
    x = ls1
    y = ls2
    plt.figure(1)
    num_bins = 100
    # the histogram of the data
    n1, bins1, patches1 = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5, label='normal')
    plt.legend(loc=2)
    # add a 'best fit' line
    x1 = mlab.normpdf(bins1, mu1, sigma1)

    n2, bins2, patches2 = plt.hist(y, num_bins, normed=1, facecolor='red', alpha=0.5, label = 'satire')
    plt.legend(loc=2)
    # add a 'best fit' line
    y2 = mlab.normpdf(bins2, mu2, sigma2)

    plt.plot(bins1, x1, 'b--')
    plt.plot(bins2, y2, 'b--')
    plt.xlabel('Variance')
    plt.ylabel('Probability')
    plt.title('Distribution of docs')
    

    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    if head == True: filename = 'dist_head.png'
    elif head == False: filename = 'dist.png'
    plt.savefig(filename, format='png')


def main():
    
    head = False
    for argv in sys.argv:
        if argv == "Head" or argv == "-H":
            head = True
    if head == True:
        ndir_path = os.getcwd() + '/vectorized_head/normal/'
        sdir_path = os.getcwd() + '/vectorized_head/satire/'
        print "Only calculate head"
    elif head == False:
        ndir_path = os.getcwd() + '/vectorized/normal/'
        sdir_path = os.getcwd() + '/vectorized/satire/'
        print "Calculate the entire doc"
    
    cnnfilels = get_file_list(ndir_path)
    ndocvls = []
    for i in range(len(cnnfilels)):
        if i%100 == 0: print "%f%% of normal finished" % (i*100*1.0/len(cnnfilels))
        f = cnnfilels[i]
        ndocvls.append(docprocess(ndir_path, f))

        
    
    onionfilels = get_file_list(sdir_path)
    sdocvls = []
    for j in range(len(onionfilels)):
        if j%100 == 0: print "%f%% of satire finished" % (j*100*1.0/len(onionfilels))
        f = onionfilels[j]
        sdocvls.append(docprocess(sdir_path, f))

    plotting(ndocvls, sdocvls, head)
    print "*****\nplotting generated\n*****"


if __name__ == "__main__":
    main()
