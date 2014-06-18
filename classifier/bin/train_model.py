#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
from sklearn.datasets import load_svmlight_file
from sklearn.svm import SVC, LinearSVC, SVR
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.externals import joblib


def parsearguments():
    parser = argparse.ArgumentParser(description='train classfication model')
    parser.add_argument('-t', '--train', action='store_true', dest='istrain', default=False)
    parser.add_argument('-l', '--load', action='store_false', dest='isload', default=True)
    return parser.parse_args()
    
def loaddata(featurefilename):
    return np.load(featurefilename)
    #return load_svmlight_file(featurefilename)

def train(train_data, train_label, test_data, test_label):
    #clf = LinearSVC(C=1.0)
    #clf = SVC(C=1.0)
    #clf = SVR(kernel='rbf', C=1.0)
    tuned_params = [{'kernel':['rbf'], 'gamma':[1e-3, 1e-4], 'C':[1,10,100,1000],},
                    {'kernel':['linear'], 'C':[1,10,100,1000]}]
    scores = ['precision', 'recall']
    clf = None
    for score in scores:
        print("# Tuning hyper-parameters for %s\n" % score)
        
        clf = GridSearchCV(SVC(C=1), tuned_params, cv=5, scoring=score)
        clf.fit(train_data, train_label)
        
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

        pred_label = clf.predict(test_data)
        print(classification_report(test_label, pred_label))
        print("")
    
    return clf

def report(clf, test_data, test_label, train_data_all, train_label_all):
    print(clf.best_estimator_)
    pred_label = clf.predict(test_data)
    print(clf.score(test_data, test_label))
    print(confusion_matrix(test_label, pred_label))
    print(accuracy_score(test_label, pred_label))
    print(classification_report(test_label, pred_label))

    
if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    args = parsearguments()
    
    FEATURE_FILE = '../data/features.txt'
    FEATURE_FILE = '../data/features.npy'
    TRAINDATA_FILE = '../data/traindata.pkl'
    LABELDATA_FILE = '../data/trainlabel.pkl'
    MODEL_FILE = '../data/catmodel.pkl'

    if args.isload:
        train_data_all = joblib.load(TRAINDATA_FILE)
        train_label_all = joblib.load(LABELDATA_FILE)
    else:
        train_data_all, train_label_all = loaddata(FEATURE_FILE)
        joblib.dump(train_data_all, TRAINDATA_FILE)
        joblib.dump(train_label_all, LABELDATA_FILE)
        
    train_data, test_data, train_label, test_label = train_test_split(train_data_all,
                                                                      train_label_all)
    
    if args.istrain:
        clf = train(train_data, train_label, test_data, test_label)
        joblib.dump(clf, modelfile)
    else:
        clf = joblib.load(modelfile)

    report(clf, test_data, test_label, train_data_all, train_label_all)
