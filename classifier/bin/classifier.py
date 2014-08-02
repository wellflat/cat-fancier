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
             meanfilename, svmmodelfile):
    
    net = caffe.Classifier(protofilename, pretrainedname,
                           mean_file=meanfilename,
                           channel_swap=(2,1,0), input_scale=255)
    net.set_phase_test()
    net.set_mode_cpu()

    estimator = joblib.load(svmmodelfile)
    clf = estimator.best_estimator_

    for imagefilename in imagelist:
        image = caffe.io.load_image(imagefilename)
        oversampled = caffe.io.oversample([caffe.io.resize_image(image, net.image_dims)],
                                          net.crop_dims)
        inputdata = np.asarray([net.preprocess('data', in_) for in_ in oversampled])
        net.forward(data=inputdata)
        feature = net.blobs['fc6wi'].data[4]
        flattenfeature = feature.flatten().tolist()
        scaledfeature = preprocessing.scale(flattenfeature)
    
        y = clf.predict(scaledfeature)
        print(labels[int(y)])

def getlabels(labelfilename):
    labels = [None]
    reader = csv.reader(file(labelfilename, 'r'), delimiter='\t', lineterminator='\n')
    for line in reader:
        labels.append(line[0])
    return labels
    

def createimagelist(imagedir):
    pattern = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
    images = [imagedir + '/' + image for image in os.listdir(imagedir) if re.match(pattern, image)]
    return images
        

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    IMAGE_FILE = '../data/test/cat/chocolat1.jpg'
    IMAGE_DIR = '../data/test/cat'
    LABEL_FILE = '../data/cat_label.tsv'
    PROTO_FILE = '../data/imagenet_feature.prototxt'
    PRETRAINED = '../data/caffe_reference_imagenet_model'
    MEAN_FILE = '../data/ilsvrc_2012_mean.npy'
    SVM_MODEL_FILE = '../data/cat_model.pkl'
    imagelist = createimagelist(IMAGE_DIR)
    labels = getlabels(LABEL_FILE)
    
    classify(imagelist, labels, PROTO_FILE, PRETRAINED, MEAN_FILE, SVM_MODEL_FILE)
