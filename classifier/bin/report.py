#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import numpy as np

def reportroc(clf, testdata, testlabel, labels):
    print('## test data shape: %s' % (testdata.shape,))
    predlabel = clf.predict(testdata)
    predprob = clf.predict_proba(testdata)
    # print(predprob[0])
    # print(predprob[0][np.argmax(predprob[0])])
    print(confusion_matrix(testlabel, predlabel))

    testlabel = label_binarize(testlabel, classes=range(1,13))
    predlabel = label_binarize(predlabel, classes=range(1,13))
    nclasses = predlabel.shape[1]
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in xrange(nclasses):
        fpr[i], tpr[i], _ = roc_curve(testlabel[:,i], predlabel[:,i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    fpr["micro"], tpr["micro"], _ = roc_curve(testlabel.ravel(), predlabel.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    plt.figure()
    plt.plot(fpr["micro"], tpr["micro"],
             label='micro-average ROC curve (area = {0:0.2f})'
             ''.format(roc_auc["micro"]))
    for i in range(nclasses):
        plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.2f})'
                 ''.format(i, roc_auc[i]))

        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Some extension of Receiver operating characteristic to multi-class')
        plt.legend(loc="lower right")
        plt.show()
    
    plt.savefig('tmp/roc')


def report(predprobfilename):
    predprob = np.load(predprobfilename)
    print(predprob)
    
if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    cmfilename = '../data/cm_rbf.npy'
    crfilename = '../data/cr_rbf.npy'
    cm = np.load(cmfilename)
    cr = np.load(crfilename)
    print(cr)

    # modelfilename = '../data/models/cat_model.pkl'
    # clf = joblib.load(modelfilename)
    # print(clf.best_estimator_)

    predprobfilename = '../data/predprob.npy'
    report(predprobfilename)
    
    norm = []
    for i in cm:
        a = 0
        tmp = []
        a = sum(i, 0)
        for j in i:
            tmp.append(float(j)/float(a))
        norm.append(tmp)
    
    fig = plt.figure(figsize=(6,4))
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    res = ax.imshow(np.array(norm), cmap=plt.cm.jet, interpolation='nearest')

    width = len(cm)
    height = len(cm[0])

    for x in xrange(width):
        for y in xrange(height):
            ax.annotate(str(cm[x][y]), xy=(y, x),
                        horizontalalignment='center',
                        verticalalignment='center')

    plt.title('cat classification')
    plt.colorbar(res)
    labels = ['Abyssinian', 'Bengal', 'Birman', 'Bombay', 'British_Shorthair', 'Egyptian_Mau', 'Maine_Coon', 'Persian', 'Ragdoll', 'Russian_Blue', 'Siamese', 'Sphynx']
    #plt.xticks(range(width), labels[:width], fontsize=10)
    plt.yticks(range(height), labels[:height], fontsize=10)
    plt.tick_params(labelbottom="off")
    plt.show()
    resultfile = './tmp/cm.png'
    plt.savefig(resultfile)
    print('save ok: %s' % (resultfile,))
