#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from sklearn.svm import LinearSVC
from sklearn.datasets import load_svmlight_file
from sklearn.externals import joblib


def createmodel(inputfilename):
    train_data, train_label = load_svmlight_file(inputfile)
    estimator = LinearSVC(C=1.0)
    print('start training.')
    estimator.fit(train_data, train_label)
    print('complete.')
    return estimator

if __name__ == '__main__':
    inputfile = '../data/_features.txt'
    outputfile = '../data/catmodel.pkl'
    # estimator = createmodel(inputfile)
    # joblib.dump(estimator, outputfile)

    loadedmodel = joblib.load(outputfile)
    print(loadedmodel)
    
    
