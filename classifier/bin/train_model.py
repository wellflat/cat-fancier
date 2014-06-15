#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
from sklearn.datasets import load_svmlight_file
from sklearn.svm import LinearSVC, SVR
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.externals import joblib


def parsearguments():
    parser = argparse.ArgumentParser(description='train classfication model')
    parser.add_argument('-t', '--train', action='store_true', dest='istrain', default=False)
    parser.add_argument('-l', '--load', action='store_false', dest='isload', default=True)
    return parser.parse_args()
    
def loaddata(featurefilename):
    return load_svmlight_file(featurefile)

def train(train_data, train_label):
    estimator = LinearSVC(C=1.0)
    #estimator = SVR(kernel='rbf', C=1.0)
    print('start training.')
    estimator.fit(train_data, train_label)
    print('complete.')
    return estimator

def validation(estimator, test_data, test_label):
    predict_label = estimator.predict(test_data)
    print(confusion_matrix(test_label, predict_label))
    print(accuracy_score(test_label, predict_label))

    
if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    args = parsearguments()
    featurefile = '../data/features.txt'
    traindatafile = '../data/traindata.pkl'
    labeldatafile = '../data/labeldata.pkl'
    modelfile = '../data/catmodel.pkl'

    if args.isload:
        train_data_all = joblib.load(traindatafile)
        label_data_all = joblib.load(labeldatafile)
    else:
        train_data_all, label_data_all = loaddata(featurefile)
        joblib.dump(train_data_all, traindatafile)
        joblib.dump(label_data_all, labeldatafile)
        
    train_data, test_data, train_label, test_label = train_test_split(train_data_all, label_data_all)
    
    if args.istrain:
        estimator = train(train_data, train_label)
        joblib.dump(estimator, modelfile)
    else:
        estimator = joblib.load(modelfile)

    validation(estimator, test_data, test_label)
    
    
    
