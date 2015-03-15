#Cosmo Zhang @ Purdue 2015/3
#Filename: senti.py
#For NLP project1
# -*- coding: utf-8 -*-

from textblob import TextBlob
import cPickle as cpcl
import numpy as np
from numpy import linalg as LA
import os
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import sys



def plotting(ls1, ls2, title):
    # ls1 normal, ls2 satire
    plt.clf() 
    mu1 = np.mean(ls1)
    mu2 = np.mean(ls2)
    sigma1 = np.std(ls1) # standard deviation of distribution
    sigma2 = np.std(ls2)
    x = ls1
    y = ls2
    plt.figure(1)
    num_bins = 50
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
    plt.xlabel('Measure')
    plt.ylabel('Density')
    plt.title('Distribution of '+title)
    

    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    filename = title+'-dist.png'
    plt.savefig(filename, format='png')

def main():
    f = open("qdata.dat", "rb")
    data = cpcl.load(f)
    f.close()
    print len(data)

    res= {"pos":{"pol":[], "sub":[]}, "neg":{"pol":[], "sub":[]}}

    for each in data:
        # print each
        text = ' '.join(each[1:-1])
        testimonial = TextBlob(text)
        pol = testimonial.sentiment.polarity
        sub = testimonial.sentiment.subjectivity
        res[each[-1]]["pol"].append(pol)
        res[each[-1]]["sub"].append(sub)

    # print res["pos"]
    plotting(res["neg"]["pol"], res["pos"]["pol"], "pol")

    plotting(res["neg"]["sub"], res["pos"]["sub"], "sub")
    print "*****\nplotting generated\n*****"

    
        


if __name__ == "__main__":
    main()
