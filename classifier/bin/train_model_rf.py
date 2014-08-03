#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import sys
import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.externals import joblib
import matplotlib.pyplot as plt

def parsearguments():
    parser = argparse.ArgumentParser(description='train classfication model')
    parser.add_argument('-t', '--train', help='train model',
                        action='store_true', dest='istrain', default=False)
    parser.add_argument('-d', '--dump', help='dump data/label pkl files',
                        action='store_true', dest='isdump', default=False)
    return parser.parse_args()

def readdata(featurefilename, labelfilename=None):
    if labelfilename is not None:
        return (np.load(featurefilename), np.load(labelfilename))    
    return load_svmlight_file(featurefilename)

def getlabels(labelfilename):
    labels = []
    reader = csv.reader(file(labelfilename, 'r'), delimiter='\t', lineterminator='\n')
    for line in reader:
        labels.append(line[0])
    return labels

def train(traindata, trainlabel, testdata, testlabel, labels):
    clf = None
    print('Start training.')
    tuned_params = [{'n_estimators': [10, 30, 50, 70, 90, 110, 130, 150], 'max_features': ['auto', 'sqrt', 'log2', None]}]
    #clf = RandomForestClassifier(n_jobs=-1)
    clf = GridSearchCV(RandomForestClassifier(), tuned_params, cv=5, scoring='accuracy', n_jobs=-1)
    clf.fit(traindata, trainlabel)
    
    print("Best parameters set found on development set:\n")
    print(clf.best_estimator_)
    print("")
    print("Grid scores on development set:\n")

    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params))
        print("")
    
    print("Detailed classification report:\n")
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.\n")
    
    predlabel = clf.predict(testdata)
    print(classification_report(testlabel, predlabel, target_names=labels))
    print("")
    print('Finish training.')
    return clf

def report(clf, testdata, testlabel, traindata_all, trainlabel_all, labels):
    print('----- Report -----')
    if hasattr(clf, 'best_estimator_'):
        print('--- best estimator:')
        print(clf.best_estimator_)
    else:
        print('--- estimator:')
        print(clf)

    # testdata = traindata_all
    # testlabel = trainlabel_all

    print('test data shape: %s' % (testdata.shape,))
    predlabel = clf.predict(testdata)
    predprob = clf.predict_proba(testdata)

    print(predprob[0])
    print(predprob[0][np.argmax(predprob[0])])
    
    #predreg = clf.predict(testdata)
    #print(clf.score(testdata, predreg))
    print('accuracy score: %s' % (accuracy_score(testlabel, predlabel),))  ## == clf.score
    cm = confusion_matrix(testlabel, predlabel)
    print(cm)
    plt.matshow(cm)
    plt.show()
    plt.savefig('tmp/cm_rf.png')
    print(classification_report(testlabel, predlabel, target_names=labels))


    
if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    args = parsearguments()
    
    FEATURE_FILE = '../data/cat_features.npy'  ## numpy.ndarray object file
    LABEL_FILE = '../data/cat_train_labels.npy'
    LABELNAME_FILE = '../data/cat_label.tsv'
    TRAINDATA_OBJFILE = '../data/train_data.pkl'
    TRAINLABEL_OBJFILE = '../data/train_labels.pkl'
    MODEL_FILE = '../data/cat_model_rf.pkl'

    labels = getlabels(LABELNAME_FILE)
    print('----- labels -----')
    print(labels)
    
    if args.isdump:
        traindata_all, trainlabel_all = readdata(FEATURE_FILE, LABEL_FILE)
        print(traindata_all.shape, trainlabel_all.shape)
        joblib.dump(traindata_all, TRAINDATA_OBJFILE)
        joblib.dump(trainlabel_all, TRAINLABEL_OBJFILE)
        print('dump files: %s , %s' % (TRAINDATA_OBJFILE, TRAINLABEL_OBJFILE))
        sys.exit(-1)
    else:
        traindata_all = joblib.load(TRAINDATA_OBJFILE)
        trainlabel_all = joblib.load(TRAINLABEL_OBJFILE)
        print('load files: %s , %s' % (TRAINDATA_OBJFILE, TRAINLABEL_OBJFILE))

    ## split arrays or matrices into random train and test subsets
    traindata, testdata, trainlabel, testlabel = train_test_split(traindata_all, trainlabel_all)
    
    if args.istrain:
        clf = train(traindata, trainlabel, testdata, testlabel, labels)
        joblib.dump(clf, MODEL_FILE)
        print('dump model: %s' % (MODEL_FILE,))
    else:
        clf = joblib.load(MODEL_FILE)
        print('load model: %s' % (MODEL_FILE,))

    report(clf, testdata, testlabel, traindata_all, trainlabel_all, labels)
