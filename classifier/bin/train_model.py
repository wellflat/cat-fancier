#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.svm import SVC, LinearSVC, SVR
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.externals import joblib
import matplotlib.pyplot as plt


def parsearguments():
    parser = argparse.ArgumentParser(description='train classfication model')
    parser.add_argument('-t', '--train', help='train model',
                        action='store_true', dest='istrain', default=False)
    parser.add_argument('-g', '--grid', help='use grid search',
                        action='store_true', dest='isgrid', default=False)
    parser.add_argument('-c', '--cv', help='number of folds (default 5)',
                        type=int, dest='cv', default=5)
    parser.add_argument('-r', '--read', help='read data/label files',
                        action='store_true', dest='isread', default=False)
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
    
def train(traindata, trainlabel, testdata, testlabel, labels, gridsearch=False, cv=5, jobs=-1):
    clf = None
    print('Start training.')
    if gridsearch:
        tuned_params = [{'kernel':['rbf'], 'gamma':[0.0, 1e-2, 1e-3, 1e-4],
                         'C':[1, 10, 100, 1000],},
                        {'kernel':['linear'], 'C':[1, 10, 100, 1000]}]
        #tuned_params = [{'kernel':['linear'], 'C':[1, 10, 100, 1000]}]
        scores = ['precision', 'recall']
        print('number of folds: %s' % (cv,))
        for score in scores:
            print("# Tuning hyper-parameters for %s\n" % score)

            svc = SVC(probability=True, verbose=False)
            clf = GridSearchCV(svc, tuned_params, cv=cv, scoring=score, n_jobs=jobs)
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
    else:
        clf = SVC(kernel='rbf', C=10, gamma=0.0001, probability=True)
        clf.fit(traindata, trainlabel)
        predlabel = clf.predict(testdata)
        print(classification_report(testlabel, predlabel, target_names=labels))

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

    print('test data shape: %s' % (testdata.shape,))
    predlabel = clf.predict(testdata)
    predprob = clf.predict_proba(testdata)

    print(predprob[0])
    print(predprob[0][np.argmax(predprob[0])])
    
    #predreg = clf.predict(testdata)
    #print(clf.score(testdata, predreg))
    print('accuracy score: %s' % (accuracy_score(testlabel, predlabel),))  ## == clf.score
    print(confusion_matrix(testlabel, predlabel))
    print(classification_report(testlabel, predlabel, target_names=labels))


    
if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    args = parsearguments()
    
    #FEATURE_FILE = '../data/features.txt'  ## libsvm format text file
    FEATURE_FILE = '../data/features.npy'  ## numpy.ndarray object file
    LABEL_FILE = '../data/labels.npy'
    LABELNAME_FILE = '../data/catlabel.tsv'
    TRAINDATA_OBJFILE = '../data/traindata.pkl'
    TRAINLABEL_OBJFILE = '../data/trainlabel.pkl'
    MODEL_FILE = '../data/catmodel.pkl'

    labels = getlabels(LABELNAME_FILE)
    print('----- labels -----')
    print(labels)
    
    if args.isread:
        #traindata_all, trainlabel_all = readdata(FEATURE_FILE)
        traindata_all, trainlabel_all = readdata(FEATURE_FILE, LABEL_FILE)
        print(traindata_all.shape, trainlabel_all.shape)
        joblib.dump(traindata_all, TRAINDATA_OBJFILE)
        joblib.dump(trainlabel_all, TRAINLABEL_OBJFILE)
    else:
        traindata_all = joblib.load(TRAINDATA_OBJFILE)
        trainlabel_all = joblib.load(TRAINLABEL_OBJFILE)

    ## split arrays or matrices into random train and test subsets
    traindata, testdata, trainlabel, testlabel = train_test_split(traindata_all, trainlabel_all)
    
    if args.istrain:
        clf = train(traindata, trainlabel, testdata, testlabel, labels, args.isgrid, args.cv)
        joblib.dump(clf, MODEL_FILE)
    else:
        clf = joblib.load(MODEL_FILE)

    report(clf, testdata, testlabel, traindata_all, trainlabel_all, labels)
