#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import caffe
import numpy as np
from sklearn import preprocessing
from pprint import pprint

def extractfeature(imagedir, labellistfilename, protofilename, pretrainedname,
                   meanfilename, featurefilename, labelfilename):
    net = caffe.Classifier(protofilename, pretrainedname, mean_file=meanfilename,
                           channel_swap=(2,1,0), input_scale=255)
    net.set_phase_test()
    net.set_mode_cpu()
    
    reader = csv.reader(file(labellistfilename, 'r'),
                        delimiter='\t', lineterminator='\n')
    #featurefile = open(featurefilename, 'w')
    features = []
    labels = []
    for line in reader:
        try:
            imagepath = imagedir + '/' + line[0]
            label = int(line[1])
            print(imagepath)
            image = caffe.io.load_image(imagepath)
            oversampled = caffe.io.oversample([caffe.io.resize_image(image, net.image_dims)],
                                              net.crop_dims)
            inputdata = np.asarray([net.preprocess('data', in_) for in_ in oversampled])
            net.forward(data=inputdata)
            feature = net.blobs['fc6wi'].data[4]
            scaledfeature = preprocessing.scale(feature.flatten().tolist())
            features.append(scaledfeature)
            labels.append(label)
            #featurefile.write("%d %s\n" % (label, ' '.join(["%d:%f" % (i, fi) for i, fi in enumerate(scaledfeature, start=1)])))
        except IOError as e:
            print(e)

    #np.save(featurefilename, features)
    np.save(labelfilename, labels)
    #featurefile.close()
    

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    IMAGE_DIR = '../../oxford_cat_images'
    LABELLIST_FILE = '../data/cat_train_label.tsv'
    PROTO_FILE = '../data/imagenet_feature.prototxt'
    PRETRAINED = '../data/caffe_reference_imagenet_model'
    MEAN_FILE = '../data/ilsvrc_2012_mean.npy'
    FEATURE_FILE = '../data/features.txt'
    FEATURE_FILE = '../data/features.npy'
    LABEL_FILE = '../data/labels.npy'
    extractfeature(IMAGE_DIR, LABELLIST_FILE, PROTO_FILE,
                   PRETRAINED, MEAN_FILE, FEATURE_FILE, LABEL_FILE)
    
