# Cosmo Zhang @ Purdue 2015/3
# Filename: nn_simple.py
# For satire, using dl
# -*- coding: utf-8 -*-

"""
Sample code for
Convolutional Neural Networks for Sentence Classification
http://ardataiv.org/pdf/1408.5882v2.pdf
"""
import cPickle
import numpy as np
from collections import defaultdict, OrderedDict
import theano
import theano.tensor as T
import re
import warnings
import sys
from nn_class import *
warnings.filterwarnings("ignore")

# different non-linearities


def ReLU(x):
    y = T.maximum(0.0, x)
    return(y)


def Sigmoid(x):
    y = T.nnet.sigmoid(x)
    return(y)


def Tanh(x):
    y = T.tanh(x)
    return(y)


def Iden(x):
    y = x
    return(y)


def getmaxl(quos):
    l = [quo["num_words"] for quo in quos]
    return np.max(l)


def train_logis_net(rng, U, dataset, sntlen = 50, n_epochs = 25, k=300, learning_rate=0.13):
    '''
    train a simple softmax
    sent_h = sentence length with padding
    sent_w = word vector length
    '''
    trainx, trainy, testx, testy = dataset

    Words = theano.shared(value = U, name = "Words")

    x = T.matrix('x')  # the data is presented as rasterized images
    # the labels are presented as 1D vector of # [int] labels
    y = T.ivector('y')

    zero_vec_tensor = T.vector()
    set_zero = theano.function([zero_vec_tensor], updates=[(Words, T.set_subtensor(Words[0,:], zero_vec_tensor))])

    classifier = LogisticRegression(input=T.cast(x.flatten(),dtype="int32"), n_in=sntlen*k, n_out=2)

    # the cost we minimize during training is the negative log likelihood of
    # the model in symbolic format
    cost = classifier.negative_log_likelihood(y)

    index = T.lscalar()
    # compiling a Theano function that computes the mistakes that are made by
    # the model on a minibatch


    test_model = theano.function(inputs = [x, y],
                                outputs=classifier.errors(y))

    validate_model = theano.function(inputs=[index],
                                    outputs=classifier.errors(y),
                                    givens={x: trainx[index:], y: trainy[index:]})


    # compute the gradient of cost with respect to theta = (W,b)
    g_W = T.grad(cost=cost, wrt=classifier.W)
    g_b = T.grad(cost=cost, wrt=classifier.b)

    # specify how to update the parameters of the model as a list of
    # (variable, update expression) pairs.
    updates = [(classifier.W, classifier.W - learning_rate * g_W),
               (classifier.b, classifier.b - learning_rate * g_b)]

    # compiling a Theano function `train_model` that returns the cost, but in
    # the same time updates the parameter of the model based on the rules
    # defined in `updates`
    train_model = theano.function(inputs=[index], outputs=cost, updates=updates,
                                  givens={x: trainx[:index], y: trainy[:index]})

    #start training over mini-batches
    print '... training'
    trlen = round(trainx.get_value(borrow = True).shape[0]*.6)
    epoch = 0
    best_val_perf = 0
    val_perf = 0
    test_perf = 0
    cost_epoch = 0
    while (epoch < n_epochs):
        epoch = epoch + 1
        cost_epoch = train_model(trlen)
        set_zero(np.zeros(k))
        train_loss = test_model(testx, testy)
        train_perf = 1 - train_loss
        val_loss = val_model(trlen)
        val_perf = 1- val_loss
        print('epoch %i, train perf %f %%, val perf %f' % (epoch, train_perf * 100., val_perf*100.))
        if val_perf >= best_val_perf:
            best_val_perf = val_perf
            test_loss = test_model(testx, testy)
            test_perf = 1- test_loss
    return test_perf


def train_mlp_net(trainset, testset):
    pass


def shared_dataset(data_xy, borrow=True):
    """
    Function that loads the dataset into shared variables

    The reason we store our dataset in shared variables is to allow
    Theano to copy it into the GPU memory (when code is run on GPU).
    Since copying data into the GPU is slow, copying a minibatch everytime
    is needed (the default behaviour if the data is not in a shared
    variable) would lead to a large decrease in performance.
    """
    data_x, data_y = data_xy
    shared_x = theano.shared(np.asarray(data_x, dtype=theano.config.floatX), borrow=borrow)
    shared_y = theano.shared(np.asarray(data_y, dtype=theano.config.floatX), borrow=borrow)
    # print data_x.shape, data_y.shape
    return shared_x, T.cast(shared_y, 'int32')


def as_floatX(variable):
    if isinstance(variable, float):
        return np.cast[theano.config.floatX](variable)

    if isinstance(variable, np.ndarray):
        return np.cast[theano.config.floatX](variable)
    return theano.tensor.cast(variable, theano.config.floatX)


def safe_update(dict_to, dict_from):
    """
    re-make update dictionary for safe updating
    """
    for key, val in dict(dict_from).iteritems():
        if key in dict_to:
            raise KeyError(key)
        dict_to[key] = val
    return dict_to


def get_idx_from_sent(sent, word_idx_map, max_l=51, k=300, filter_h=5):
    """
    Transforms sentence into a list of indices. Pad with zeroes.
    """
    pad = filter_h - 1
    x = [0 for i in xrange(pad)]
    for word in sent:
        try:
            x.append(word_idx_map[word])
        except:
            print "Error, word not in the map"
            sys.exit("Please debug")
    while len(x) < max_l + 2 * pad:  # to make sure the length is max_l + 2*pad
        x.append(0)
    return x  # an list of word indices


def make_idx_data_cv(quos, word_idx_map, cv, max_l=51, k=300, filter_h=5):
    """
    Transforms sentences into a 2-d matrix.
    """
    trainx, trainy, testx, testy = [], [], [], []
    for quo in quos:
        sent = get_idx_from_sent(quo["text"], word_idx_map, max_l, k, filter_h)
        if quo["split"] == cv:
            testx.append(sent)
            testy.append(quo["y"])
        else:
            trainx.append(sent)
            trainy.append(quo["y"])
    train = [np.array(trainx, dtype="int"), np.array(trainy, dtype="int")]
    test = [np.array(testx, dtype="int"), np.array(testy, dtype="int")]
    return (train, test)


def main():
    print "loading data...",
    data = cPickle.load(open("data4use.dat", "rb"))
    quos, W, W2, word_idx_map, vocab = data[0], data[1], data[2], data[3], data[4]
    print "data loaded!"
    '''
    mode= sys.argv[1]
    word_vectors = sys.argv[2]
    if mode=="-nonstatic":
        print "model architecture: CNN-non-static"
        non_static=True
    elif mode=="-static":
        print "model architecture: CNN-static"
        non_static=False
    execfile("conv_net_classes.py")
    if word_vectors=="-rand":
        print "using: random vectors"
        U = W2
    elif word_vectors=="-word2vec":
        print "using: word2vec vectors"
        U = W
    '''
    max_l = getmaxl(quos)

    non_static = False
    U = W
    results = []
    r = range(0, 10)
    rng = np.random.RandomState(3435)  # random number generator
    for i in r:
        trainset, testset = make_idx_data_cv(quos, word_idx_map, i, max_l=max_l, k=300, filter_h=5)
        trainx, trainy = shared_dataset(trainset)
        testx, testy = shared_dataset(testset)
        # print trainx, trainy, testx, testy
        dataset = (trainx, trainy, testx, testy)
        '''
        training
        '''
        acc1 = train_logis_net(rng, U, dataset, sntlen=max_l, k=300)  # softmax
        # acc2 = train_mlp_net(rng, dataset, sntlen=max_l)  # mlp
        print "cv: " + str(i) + ", logis performance: " + str(acc1) + ", mlp performance" + str(acc2)
        results.append((acc1, acc2))
    print "Overall logis performance: " + str(np.mean([res[0] for res in results]))
    print "Overall mlp performance: " + str(np.mean([res[1] for res in results]))

if __name__ == "__main__":
    main()
