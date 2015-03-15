#Cosmo Zhang @ Purdue 2015/3
#filename: genquota.py
#for nlp satire
# -*- coding: utf-8 -*-


import cPickle as cpcl



def main():
    f = open("data.dat", "rb")
    data = cpcl.load(f)
    f.close()

    newset = []
    for each in data:
        for quota in each[0]:
            newset.append([quota[0], quota[1:], each[1]])#each[1] is the category label
            
    print newset[1]

            
    g = open("qdata.dat", "wb")
    cpcl.dump(newset, g)
    g.close()


if __name__ == "__main__":
    main()
