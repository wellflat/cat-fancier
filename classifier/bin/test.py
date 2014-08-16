#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import caffe
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

def classify(modelfilename, pretrainedname, meanfilename,
             imagefilename, labelfilename, dstdir):
    plt.rcParams['figure.figsize'] = (10,10)
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'
    
    mean = np.load(meanfilename)
    net = caffe.Classifier(modelfilename, pretrainedname, mean=mean,
                           channel_swap=(2,1,0), image_dims=(256,256), raw_scale=255)
    inputimage = caffe.io.load_image(imagefilename)
    #plt.imshow(inputimage)

    # Resize the image to the standard (256, 256) and oversample net input sized crops.
    #oversampled = caffe.io.oversample([caffe.io.resize_image(inputimage, net.image_dims)], net.crop_dims)
    # 'data' is the input blob name in the model definition, so we preprocess for that input.
    #inputdata = np.asarray([net.preprocess('data', in_) for in_ in oversampled])
    # forward() takes keyword args for the input blobs with preprocessed input arrays.
    #net.forward(data=inputdata)
    
    prediction = net.predict([inputimage], oversample=True)
    print('prediction shape: ', prediction[0].shape)
    print('predicted class: ', prediction[0].argmax())

    plt.imshow(net.deprocess('data', net.blobs['data'].data[4]))

    # filters = net.params['conv1'][0].data
    # vis_square(filters.transpose(0,2,3,1))

    layers = [(k,v.data.shape) for k, v in net.blobs.items()]
    pprint(layers)
    layers = [(k,v[0].data.shape) for k, v in net.params.items()]
    pprint(layers)
    
    labels = np.loadtxt(labelfilename, str, delimiter='\t')
    top_k = net.blobs['prob'].data[4].flatten().argsort()[-1:-6:-1]
    print(labels[top_k])

    #feat = net.blobs['fc6wi'].data[4]
    feat = net.blobs['fc6i'].data[4]
    plt.subplot(2,1,1)
    plt.plot(feat.flat)
    plt.subplot(2,1,2)
    _ = plt.hist(feat.flat[feat.flat > 0], bins=100)
    print(feat.shape)
    print(feat.flat[0:100])
    plt.savefig(dstdir + 'test2.jpg')

# take an array of shape (n, height, width) or (n, height, width, channels)
#  and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    plt.imshow(data)


def predprobreport(predprobfilename):
    predprob = np.load(predprobfilename)
    print(len(predprob[0]))

    
if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    MODEL_FILE = '../data/imagenet_feature.prototxt'
    PRETRAINED = '../data/caffe_reference_imagenet_model'
    IMAGE_FILE = '../../cat_images/Abyssinian_2.jpg'
    #IMAGE_FILE = '../data/cat.jpg'
    LABEL_FILE = '../data/synset_words.txt'
    MEAN_FILE = '../data/ilsvrc_2012_mean.npy'
    DST_DIR = '/var/www/html/tmp/'
    PRED_PROB = '../data/predprob.npy'
    #classify(MODEL_FILE, PRETRAINED, MEAN_FILE, IMAGE_FILE, LABEL_FILE, DST_DIR)
    predprobreport(PRED_PROB)
