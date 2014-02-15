#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import cv2 as cv

def parsearguments():
    parser = argparse.ArgumentParser(description='object detection using cascade classifier')
    parser.add_argument('imagefilename', help='image file name')
    parser.add_argument('cascadefilename', help='cascade file name')
    parser.add_argument('-o', '--output', dest='output')
    return parser.parse_args()

def detect(imagefilename, cascadefilename):
    srcimg = cv.imread(imagefilename)
    cascade = cv.CascadeClassifier(cascadefilename)
    objects = cascade.detectMultiScale(srcimg, 1.1, 3)
    for (x, y, w, h) in objects:
        print(x, y, w, h)
        cv.rectangle(srcimg, (x, y), (x + w, y + h), (0, 0, 255), 4)
    return srcimg

if __name__ == '__main__':
    args = parsearguments()
    result = detect(args.imagefilename, args.cascadefilename)
    cv.imwrite('box/detect.jpg', result)
    
    

