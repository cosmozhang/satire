import cPickle
from treeUtil import *
from numpy import *
import nltk.classify.util
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression


def forward_prop(params, tree, labels=True):

    tree.reset_finished()
    err_sum = 0.0

    (WL, WR, W_label, b1, b_label, L) = params

    # forward prop
    to_do = tree.get_leaves()
    while to_do:

        curr = to_do.pop(0)

        # node is leaf
        if curr.c1 is None:

            # activation function is  tanh
            curr.p_norm = curr.vec

        else:
            curr.p = tanh(WL.dot(curr.c1.p_norm) + WR.dot(curr.c2.p_norm) + b1) 
            curr.p_norm = curr.p / linalg.norm(curr.p)

        curr.finished = 1     

        if labels:
            curr.classification = util.softmax((W_label.dot(curr.p_norm) + b_label) ) 
            curr.error = util.crossent(tree.label.reshape( (2, 1)), curr.classification)
            curr.delta = util.crossent_loss(tree.label.reshape( (2, 1)) , curr.classification)  
            err_sum += curr.error
            
        if curr.parent != None and curr.parent.c1.finished and curr.parent.c2.finished:
            to_do.append(curr.parent)

    return err_sum


def validate(trees, params):

    print 'computing sentence representations...'

    stop = stopwords.words('english')
    (WL, WR, W_label, b1, b_label, L) = params
    feats = []

    for tree in trees:
        leaves = tree.get_leaves()
        for leaf in leaves:
            leaf.vec = (L[:, leaf.ind]).reshape( (d, 1)) 

        forward_prop(params, tree, labels=False)
        label = 'Conservative'
        if tree.label[0] == 1:
            label = 'Liberal'

        w_ave = zeros((d, 1))
        w_count = 0

        n_ave = zeros((d, 1))
        n_count = 0
        for node in tree:

            if isinstance(node, leafObj) and node.word not in stop:
                w_ave += node.vec
                w_count += 1.

            n_ave += node.p_norm
            n_count += 1.

        w_ave /= w_count
        n_ave /= n_count

        featvec = concatenate([w_ave.flatten(), n_ave.flatten()])
        curr_feats = {}
        for dim, val in ndenumerate(featvec):
            curr_feats['__' + str(dim)] = val

        feats.append( (curr_feats, label) )

    print 'training...'
    classifier = SklearnClassifier(LogisticRegression(C=100))
    classifier.train(feats)
    print 'training accuracy:', nltk.classify.util.accuracy(classifier, feats)


if __name__ == '__main__':

    trees, vocab = cPickle.load(open('ibc_trees', 'rb'))
    print len(trees)
    d = 100
    params = cPickle.load( open('ibc_params', 'rb'))
    validate(trees, params)