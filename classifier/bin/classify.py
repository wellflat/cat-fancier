#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import re
import caffe
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.datasets import load_svmlight_file
from sklearn.externals import joblib
import pylab as pl

def classify(imagelist, labeldata, modelfilename, pretrainedname,
             meanfilename, svmmodelfile, resultimagename):
    
    net = caffe.Classifier(modelfilename, pretrainedname,
                           mean_file=meanfilename,
                           channel_swap=(2,1,0), input_scale=255)
    net.set_phase_test()
    net.set_mode_cpu()

    estimator = joblib.load(svmmodelfile)

    for imagefilename in imagelist:
        image = caffe.io.load_image(imagefilename)
        oversampled = caffe.io.oversample([caffe.io.resize_image(image, net.image_dims)],
                                          net.crop_dims)
        caffeinput = np.asarray([net.preprocess('data', in_) for in_ in oversampled])
        net.forward(data=caffeinput)
        feat = net.blobs['fc6wi'].data[4]
        flattenfeat = feat.flatten().tolist()
    
        y = estimator.predict(flattenfeat)
        print(labeldata[int(y)])

def getlabels(labelfilename):
    labeldata = [None]
    reader = csv.reader(file(labelfilename, 'r'), delimiter='\t', lineterminator='\n')
    for line in reader:
        labeldata.append(line[0])
    return labeldata
    

def createimagelist(imagedir):
    pattern = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
    images = [imagedir + '/' + image for image in os.listdir(imagedir) if re.match(pattern, image)]
    return images
        

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    #IMAGE_FILE = '../../oxford_cat_images/Maine_Coon_1.jpg'
    IMAGE_FILE = '../data/test/cat/chocolat1.jpg'
    IMAGE_DIR = '../data/test/cat'
    LABEL_FILE = '../data/catlabel.tsv'
    MODEL_FILE = '../data/imagenet_feature.prototxt'
    PRETRAINED = '../data/caffe_reference_imagenet_model'
    MEAN_FILE = '../data/ilsvrc_2012_mean.npy'
    SVM_MODEL_FILE = '../data/catmodel.pkl'
    RESULT_IMAGE = '../tmp/svr.png'
    imagelist = createimagelist(IMAGE_DIR)
    labeldata = getlabels(LABEL_FILE)
    classify(imagelist, labeldata, MODEL_FILE, PRETRAINED, MEAN_FILE, SVM_MODEL_FILE, RESULT_IMAGE)
