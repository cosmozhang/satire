import numpy as np
import cPickle as cpcl
from collections import defaultdict
import sys
import re
import pandas as pd
from nltk.tokenize import word_tokenize


def build_data_cv(filename, cv=10, speaker = True):
    """
    Loads data and split into 10 folds.
    """
    quos = []
    vocab = defaultdict(float)
    with open(filename, "rb") as f:
        quodata = cpcl.load(f)
        for eg in quodata:
            if speaker:
                wlist = clean_str(eg[0] + ' ' +' '.join(eg[1]))
            else:
                wlist = clean_str(' '.join(eg[1]))
            for word in wlist:
                vocab[word] += 1
            if eg[-1] == "pos":
                    y = 1
            elif eg[-1] == "neg":
                    y = 0
            datum = {"y": 1,
                     "text": wlist,
                     "num_words": len(wlist),
                     "split": np.random.randint(0, cv)}
            quos.append(datum)
    return quos, vocab


def get_W(word_vecs, k=300):
    """
    Get word matrix. W[i] is the vector for word indexed by i
    """
    vocab_size = len(word_vecs) #the updated vocab_size
    word_idx_map = dict()
    W = np.zeros(shape=(vocab_size + 1, k)) #W is the word matrix
    W[0] = np.ones(k)
    i = 1 #W[0] is the bias intercept
    for word in word_vecs:
        W[i] = word_vecs[word]
        word_idx_map[word] = i
        i += 1
    return W, word_idx_map

#function to read-in the word vector bin file
def load_bin_vec(fname, vocab):
    """
    Loads 300x1 word vecs from Google (Mikolov) word2vec
    """
    word_vecs = {}
    with open(fname, "rb") as f:
        header = f.readline()
        vocab_size, layer1_size = map(int, header.split())
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in xrange(vocab_size):
            word = []
            while True:
                ch = f.read(1)
                if ch == ' ':
                    word = ''.join(word)
                    break
                if ch != '\n':
                    word.append(ch)
            if word in vocab:
                word_vecs[word] = np.fromstring(
                    f.read(binary_len), dtype='float32')
            else:
                f.read(binary_len)
    return word_vecs


def add_unknown_words(word_vecs, vocab, min_df=1, k=300):
    """
    For words that occur in at least min_df documents, create a separate word vector.
    0.25 is chosen so the unknown vectors have (approximately) same variance as pre-trained ones
    """
    for word in vocab:
        if word not in word_vecs and vocab[word] >= min_df: #min_df is the minimum appearance count
            word_vecs[word] = np.random.uniform(-0.25, 0.25, k)


def clean_str(string, TREC=False):
    wlst = word_tokenize(string)
    if TREC:
        return wlst
    else:
        # return [word.lower() for word in wlst]
        return [word for word in wlst]

    """
    Tokenization/string cleaning for all datasets except for SST.
    Every dataset is lower cased except for TREC

    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    """

def clean_str_sst(string):
    """
    Tokenization/string cleaning for the SST dataset
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def main():
    if len(sys.argv) < 3:
        print "Usage: python process_data.py [data file] [w2v file]"
        sys.exit("Not enough arguments")
    data_filename = sys.argv[1]
    w2v_filename = sys.argv[2]
    print "loading data...",
    quos, vocab = build_data_cv(data_filename) #all the quotes and all the words as the dictionary vocab
    max_l = np.max(pd.DataFrame(quos)["num_words"]) #max length of all the examples
    print "data loaded!"
    print "number of quotes: " + str(len(quos))
    print "vocab size: " + str(len(vocab))
    print "max sentence length: " + str(max_l)
    print "loading word2vec vectors...",
    w2v = load_bin_vec(w2v_filename, vocab) #dictionary contains the
    print "word2vec loaded!"
    print "num words already in word2vec: " + str(len(w2v)) #the original length
    add_unknown_words(w2v, vocab)
    W, word_idx_map = get_W(w2v) # using word vectors from mikolov, while word not in the bin are randomly initialized
    rand_vecs = {}
    add_unknown_words(rand_vecs, vocab)
    W2, _ = get_W(rand_vecs) # all words are of randomized vectors
    cpcl.dump([quos, W, W2, word_idx_map, vocab], open("data4use.dat", "wb"))
    print "dataset created!"


if __name__ == "__main__":
    main()
