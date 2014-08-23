#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import re
import caffe
import numpy as np
from sklearn import preprocessing
from sklearn.externals import joblib

def classify(imagelist, labels, protofilename, pretrainedname,
             meanfilename, modelfilename):
    mean = np.load(meanfilename)
    net = caffe.Classifier(protofilename, pretrainedname, mean=mean,
                           channel_swap=(2,1,0), image_dims=(256,256), raw_scale=255)
    print('# ----- Target labels -----')
    print(labels)
    
    estimator = joblib.load(modelfilename)
    clf = estimator.best_estimator_
    print(clf)
    features = []
    for imagefilename in imagelist:
        image = caffe.io.load_image(imagefilename)
        oversampled = caffe.io.oversample([caffe.io.resize_image(image, net.image_dims)],
                                          net.crop_dims)
        inputdata = np.asarray([net.preprocess('data', in_) for in_ in oversampled])
        net.forward(data=inputdata)
        feature = net.blobs['fc6i'].data[4]
        flattenfeature = feature.flatten().tolist()
        scaledfeature = preprocessing.scale(flattenfeature)
        features.append(scaledfeature)

    predlabels = clf.predict(features)
    predprobas = clf.predict_proba(features)
    print(predprobas)
    topk = predprobas.argsort()[0][-1:-6:-1]
    pred = zip(labels[topk], predprobas[0][topk])
    print(pred)

    

def getlabels(labelfilename):
    #labels = [None]
    labels = []
    reader = csv.reader(file(labelfilename, 'r'), delimiter='\t', lineterminator='\n')
    for line in reader:
        labels.append(line[0])
    return np.array(labels)
    

def createimagelist(imagedir):
    pattern = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
    images = [imagedir + '/' + image for image in os.listdir(imagedir) if re.match(pattern, image)]
    return images
        

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    IMAGE_FILE = '../data/cat_images/Bombay_6.jpg'
    IMAGE_DIR = '../../cat_test_images'
    LABEL_FILE = '../data/cat_label.tsv'
    PROTO_FILE = '../data/imagenet_feature.prototxt'
    PRETRAINED = '../data/caffe_reference_imagenet_model'
    MEAN_FILE = '../data/ilsvrc_2012_mean.npy'
    MODEL_FILE = '../data/models/cat_model_lr.pkl'
    imagelist = createimagelist(IMAGE_DIR)
    imagelist = [IMAGE_FILE]
    labels = getlabels(LABEL_FILE)
    
    classify(imagelist, labels, PROTO_FILE, PRETRAINED, MEAN_FILE, MODEL_FILE)
