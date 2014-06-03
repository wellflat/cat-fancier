#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import re

def createlabels(imagedir, labeldata, labelfilename):
    labelfile = open(labelfilename, 'w')
    for key, label in labeldata.iteritems():
        pattern = re.compile(key)
        images = [image for image in os.listdir(imagedir) if re.match(pattern, image)]
        print(key,label)
        print(len(images))
        for image in images:
            labelstr = '%s,%s\n' % (image, label)
            #print(labelstr)
            labelfile.write(labelstr)

    labelfile.close()
            

if __name__ == '__main__':
    labelfile = 'cat_train_label.csv'
    labeldata = {'Abyssinian':1, 'Bengal':2, 'Birman':3, 'Bombay':4, 'British_Shorthair':5, 'Egyptian_Mau':6, 'Maine_Coon':7, 'Persian':8, 'Ragdoll':9, 'Russian_Blue':10, 'Siamese':11, 'Sphynx':12}
    imagedir = '../images'
    createlabels(imagedir, labeldata, labelfile)
    
