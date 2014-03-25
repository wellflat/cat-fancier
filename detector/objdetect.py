#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
import cv2 as cv

def parsearguments():
    parser = argparse.ArgumentParser(description='object detection using cascade classifier')
    parser.add_argument('imagefilename', help='image file name')
    parser.add_argument('-c', '--cascade', dest='cascadefilename', help='cascade file name',
                        default='models/cat/lbp/cascade.xml')
    parser.add_argument('-s', '--scale', dest='scalefactor', type=float, default=1.1)
    parser.add_argument('-n', '--neighbors', dest='minneighbors', type=int, default=3)
    parser.add_argument('-o', '--output', dest='output',
                        default='box/detect.jpg')
    return parser.parse_args()

def detect(imagefilename, cascadefilename, scalefactor, minneighbors):
    srcimg = cv.imread(imagefilename)
    if srcimg is None:
        print('cannot load image')
        sys.exit(-1)
    cascade = cv.CascadeClassifier(cascadefilename)
    objects = cascade.detectMultiScale(srcimg, scalefactor, minneighbors)
    for (x, y, w, h) in objects:
        print(x, y, w, h)
        cv.rectangle(srcimg, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return srcimg

if __name__ == '__main__':
    args = parsearguments()
    result = detect(args.imagefilename, args.cascadefilename,
                    args.scalefactor, args.minneighbors)
    cv.imwrite(args.output, result)
