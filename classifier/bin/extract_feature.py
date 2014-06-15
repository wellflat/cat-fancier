#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import caffe
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from pprint import pprint

def extractfeature(imagedir, labelfilename, modelfilename, pretrainedname,
                   meanfilename, featurefilename):
    net = caffe.Classifier(modelfilename, pretrainedname,
                           mean_file=meanfilename,
                           channel_swap=(2,1,0), input_scale=255)
    net.set_phase_test()
    net.set_mode_cpu()
    
    reader = csv.reader(file(labelfilename, 'r'), delimiter='\t', lineterminator='\n')
    featurefile = open(featurefilename, 'w')
    for line in reader:
        try:
            imagepath = imagedir + '/' + line[0]
            print(imagepath)
            image = caffe.io.load_image(imagepath)
            oversampled = caffe.io.oversample([caffe.io.resize_image(image, net.image_dims)],
                                              net.crop_dims)
            caffeinput = np.asarray([net.preprocess('data', in_) for in_ in oversampled])
            net.forward(data=caffeinput)
            feat = net.blobs['fc6wi'].data[4]
            print(feat.flatten().tolist())
            scaledfeat = preprocessing.scale(feat.flatten().tolist())
            print(scaledfeat)
            #featurefile.write("%d %s\n" % (int(line[1]), ' '.join(["%d:%f" % (i, fi) for i, fi in enumerate(feat.flatten().tolist(), start=1)])))
            featurefile.write("%d %s\n" % (int(line[1]), ' '.join(["%d:%f" % (i, fi) for i, fi in enumerate(scaledfeat, start=1)])))
        except IOError as e:
            print(e)
    featurefile.close()
    

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    IMAGE_DIR = '../../oxford_cat_images'
    LABEL_FILE = '../data/cat_train_label.tsv'
    MODEL_FILE = '../data/imagenet_feature.prototxt'
    PRETRAINED = '../data/caffe_reference_imagenet_model'
    MEAN_FILE = '../data/ilsvrc_2012_mean.npy'
    FEATURE_FILE = '../data/features.txt'
    extractfeature(IMAGE_DIR, LABEL_FILE, MODEL_FILE, PRETRAINED, MEAN_FILE, FEATURE_FILE)
    
