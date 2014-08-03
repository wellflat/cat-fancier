#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import caffe
import numpy as np
from sklearn import preprocessing
from pprint import pprint

def extractfeature(imagedir, labellistfilename, protofilename, pretrainedname,
                   meanfilename, featurefilename, labelfilename, libsvmformat=False):

    print('Start extract features.')
    net = caffe.Classifier(protofilename, pretrainedname, mean_file=meanfilename,
                           channel_swap=(2,1,0), input_scale=255)
    net.set_phase_test()
    net.set_mode_cpu()
    
    reader = csv.reader(file(labellistfilename, 'r'),
                        delimiter='\t', lineterminator='\n')
    if libsvmformat:
        print('output: libsvm format')
        featurefile = open(featurefilename, 'w')
    else:
        print('output: npy format')
    print('image dims: %s' % (net.image_dims,))
    features = []
    labels = []
    for line in reader:
        try:
            imagepath = imagedir + '/' + line[0]
            label = int(line[1])
            print(imagepath, label)
            image = caffe.io.load_image(imagepath)
            oversampled = caffe.io.oversample([caffe.io.resize_image(image, net.image_dims)],
                                              net.crop_dims)
            inputdata = np.asarray([net.preprocess('data', in_) for in_ in oversampled])
            net.forward(data=inputdata)
            feature = net.blobs['fc6wi'].data[4]
            scaledfeature = preprocessing.scale(feature.flatten().tolist())
            if libsvmformat:
                featurefile.write("%d %s\n" % (label, ' '.join(["%d:%f" % (i, fi) for i, fi in enumerate(scaledfeature, start=1)])))
            else:
                features.append(scaledfeature)
                labels.append(label)
        except IOError as e:
            print(e)

    np.save(featurefilename, features)
    np.save(labelfilename, labels)
    if featurefile_ext == '.txt':
        featurefile.close()

    print('Finish extract features.')
    

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    IMAGE_DIR = '../../cat_images'
    LABELLIST_FILE = '../data/cat_train_labels.tsv'
    PROTO_FILE = '../data/imagenet_feature.prototxt'
    PRETRAINED_FILE = '../data/caffe_reference_imagenet_model'
    MEAN_FILE = '../data/ilsvrc_2012_mean.npy'
    FEATURE_FILE = '../data/cat_features.txt'  ## libsvm format file
    FEATURE_FILE = '../data/cat_features.npy'
    LABEL_FILE = '../data/cat_train_labels.npy'
    featurefile_ext = os.path.splitext(FEATURE_FILE)[-1]
    if featurefile_ext == '.txt':
        libsvmformat = True
    else:
        libsvmformat = False
    extractfeature(IMAGE_DIR, LABELLIST_FILE, PROTO_FILE,
                   PRETRAINED_FILE, MEAN_FILE, FEATURE_FILE, LABEL_FILE, libsvmformat)
    
