#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import re

def writetrainlabels(imagedir, labeldata, labelfilename):
    labelfile = open(labelfilename, 'w')
    for key, label in labeldata.iteritems():
        pattern = re.compile(key)
        images = [image for image in os.listdir(imagedir) if re.match(pattern, image)]
        print(key,label)
        print(len(images))
        for image in images:
            labelstr = '%s\t%s\n' % (image, label)
            #print(labelstr)
            labelfile.write(labelstr)

    labelfile.close()

def readlabels(filename):
    import csv
    labeldata = {}
    reader = csv.reader(file(filename, 'r'), delimiter='\t', lineterminator='\n')
    for line in reader:
        labeldata[line[0]] = int(line[1])
    return labeldata
            

if __name__ == '__main__':
    labelfile = '../data/cat_train_label.tsv'
    labeldata = readlabels('../data/catlabel.tsv')
    imagedir = '../../cat_images'
    writetrainlabels(imagedir, labeldata, labelfile)
    
