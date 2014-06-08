#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import caffe
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.datasets import load_svmlight_file
from sklearn.externals import joblib

def classify(imagefilename, modelfilename, pretrainedname, meanfilename, svmmodelfile):
    net = caffe.Classifier(modelfilename, pretrainedname,
                           mean_file=meanfilename,
                           channel_swap=(2,1,0), input_scale=255)
    net.set_phase_test()
    net.set_mode_cpu()

    image = caffe.io.load_image(imagefilename)
    oversampled = caffe.io.oversample([caffe.io.resize_image(image, net.image_dims)],
                                      net.crop_dims)
    caffeinput = np.asarray([net.preprocess('data', in_) for in_ in oversampled])
    net.forward(data=caffeinput)
    feat = net.blobs['fc6wi'].data[4]
    flattenfeat = feat.flatten().tolist()

    estimator = joblib.load(svmmodelfile)
    label = estimator.predict(flattenfeat)
    print(label)
    
        

if __name__ == '__main__':
    IMAGE_FILE = '../../cat_images/Maine_Coon_1.jpg'
    MODEL_FILE = '../data/imagenet_feature.prototxt'
    PRETRAINED = '../data/caffe_reference_imagenet_model'
    MEAN_FILE = '../data/ilsvrc_2012_mean.npy'
    SVM_MODEL_FILE = '../data/catmodel.pkl'
    classify(IMAGE_FILE, MODEL_FILE, PRETRAINED, MEAN_FILE, SVM_MODEL_FILE)
