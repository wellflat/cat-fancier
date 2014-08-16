#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import sys
import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.svm import SVC, LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.externals import joblib
import matplotlib.pyplot as plt


def parsearguments():
    parser = argparse.ArgumentParser(description='train classfication model')
    parser.add_argument('-t', '--train', help='train model',
                        action='store_true', dest='istrain', default=False)
    parser.add_argument('-m', '--model', help='model type (default lr)',
                        type=str, dest='modeltype', default='lr')
    parser.add_argument('-c', '--cv', help='number of folds (default 5)',
                        type=int, dest='cv', default=5)
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
    
def train(traindata, trainlabel, testdata, testlabel, labels,
          modeltype='lr', cv=5, jobs=-1):
    clf = None
    print('---------- Start training. ----------')
    if modeltype == 'lr':    ## Logistic Regression
        print('# Logistic Regression model')
        #tuned_params = [{'C':np.logspace(-5, -4, 5),},]
        tuned_params = [{'C':[0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,0.0009,0.001],},]
        model = LogisticRegression()
    elif modeltype == 'rbf': ## SVM RBF kernel
        print('# SVM (RBF kernel) model')
        tuned_params = [{'kernel':['rbf'], 'C':np.logspace(0, 2, 10),
                         'gamma':np.logspace(-5, -3, 10)},]
        model = SVC(probability=False)
    elif modeltype == 'rf':  ## Random Forest
        print('# Random Forest model')
        tuned_params = [{'n_estimators': range(100, 200, 10),
                         'max_features': ['auto', 'log2']}]  ## auto == sqrt
        model = RandomForestClassifier(oob_score=True, n_jobs=jobs)
    else:
        print('model type: [lr|rbf|rf]')
        sys.exit(-1)
        
    print('# number of folds: %s' % (cv,))
    print('# params grid: %s' % (tuned_params,))

    print("# Tuning hyper-parameters for accuracy\n")

    clf = GridSearchCV(model, tuned_params, cv=cv, scoring='accuracy', n_jobs=jobs, verbose=10)
    clf.fit(traindata, trainlabel)
        
    print("# Best parameters set found on development set:\n")
    print(clf.best_estimator_)
    print("")
    print("# Grid scores on development set:\n")
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params))
    print("")

    print("# Detailed classification report:\n")
    print("")
    predlabel = clf.predict(testdata)
    print(classification_report(testlabel, predlabel, target_names=labels))
    print('---------- Finish training. ----------')
    return clf

def report(clf, testdata, testlabel, traindata_all, trainlabel_all, labels,
           reportdir, modeltype, istrain=False):
    print('# ----- Classification report -----')
    if hasattr(clf, 'best_estimator_'):
        print('## --- best estimator:')
        print(clf.best_estimator_)
    else:
        print('## --- estimator:')
        print(clf)

    print('## test data shape: %s' % (testdata.shape,))
    predlabel = clf.predict(testdata)
    
    print('## accuracy: %s' % (accuracy_score(testlabel, predlabel),))  ## == clf.score
    cm = confusion_matrix(testlabel, predlabel)
    print('## confusion matrix')
    print(cm)
    cr = classification_report(testlabel, predlabel, target_names=labels)
    print(cr)

    if istrain:
        print('save report files')
        np.save(reportdir + 'cm_' + modeltype, cm)
        np.save(reportdir + 'cr_' + modeltype, cr)


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    args = parsearguments()
    
    #FEATURE_FILE = '../data/cat_features.txt'  ## libsvm format text file
    FEATURE_FILE = '../data/cat_features.npy'  ## numpy.ndarray object file
    LABEL_FILE = '../data/cat_train_labels.npy'
    LABELNAME_FILE = '../data/cat_label.tsv'
    TRAINDATA_OBJFILE = '../data/train_data.pkl'
    TRAINLABEL_OBJFILE = '../data/train_labels.pkl'
    #MODEL_FILE = '../data/models/cat_model.pkl'  ## SVM rbf
    MODEL_FILE = '../data/models/cat_model_lr.pkl'
    #MODEL_FILE = '../data/models/cat_model_rf.pkl'
    REPORT_DIR = '../data/'

    labels = getlabels(LABELNAME_FILE)
    print('# ----- Target labels -----')
    print(labels)
    
    if args.isdump:
        #traindata_all, trainlabel_all = readdata(FEATURE_FILE)
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
        clf = train(traindata, trainlabel, testdata, testlabel, labels, args.modeltype, args.cv)
        joblib.dump(clf, MODEL_FILE)
        print('dump model: %s' % (MODEL_FILE,))
    else:
        clf = joblib.load(MODEL_FILE)
        print('load model: %s' % (MODEL_FILE,))

    # report(clf, testdata, testlabel, traindata_all, trainlabel_all, labels,
    #        REPORT_DIR, args.modeltype, args.istrain)
    report2(clf, traindata_all, trainlabel_all, labels)
