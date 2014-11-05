import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

'''
    pl.figure(num)
    p1, =pl.plot(x[0], ls[0], color="red", marker='s', ls="--", ms=10)
    p2, =pl.plot(x[1], ls[1], color="blue", marker='o', ls="--", ms=10)
    p3, =pl.plot(x[2], ls[2], color="green", marker='v', ls="--", ms=10)
    p4, =pl.plot(x[3], ls[3], color="orange", marker='^', ls="--", ms=10)
    pl.xticks(np.arange(min(min(x[0]), min(x[1]), min(x[2]), min(x[3]))-0.1, max(max(x[0]), max(x[1]), max(x[2]), max(x[3]))+0.1, 0.1))
    pl.xlim((min(min(x[0]), min(x[1]), min(x[2]), min(x[3]))-0.1, max(max(x[0]), max(x[1]), max(x[2]), max(x[3]))+0.1))
    pl.ylim((min(ls[0]+ls[1]+ls[2]+ls[3])-0.1,max(ls[0]+ls[1]+ls[2]+ls[3])+0.1))
    #pl.yticks(np.arange(min(ls[0]+ls[1]+ls[2]+ls[3])-0.1,max(ls[0]+ls[1]+ls[2]+ls[3])+0.1, 0.05))
    pl.legend([p1,p2,p3,p4], ["8x8", "4x4x4", "zig-zag", "binary"], loc=0)
    pl.xlabel("Acceptable Error Threshold")
    pl.ylabel(name)
    
    pl.title(name+" v.s. Acceptable Error Threshold")
    filename=name+".png"
    pl.savefig(filename, format='png')
    #print m,d
    print "plotting ok"
'''

# example data
mu1 = 100 # mean of distribution
mu2 = 200
sigma = 15 # standard deviation of distribution
x = mu1 + sigma * np.random.randn(10000)
y = mu2 + sigma * np.random.randn(10000)
plt.figure(1)
num_bins = 100
# the histogram of the data
n1, bins1, patches1 = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
# add a 'best fit' line
x1 = mlab.normpdf(bins1, mu1, sigma)

n2, bins2, patches2 = plt.hist(y, num_bins, normed=1, facecolor='red', alpha=0.5)
# add a 'best fit' line
y2 = mlab.normpdf(bins2, mu2, sigma)

plt.plot(bins1, x1, 'b--')
plt.plot(bins2, y2, 'b--')
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)
plt.savefig('testme.png', format='png')

