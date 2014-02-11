#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import cv2 as cv

def detect(filename, cascadefilename='cascade.xml'):
    srcimg = cv.imread(filename)
    cascade = cv.CascadeClassifier(cascadefilename)
    objects = cascade.detectMultiScale(srcimg, 1.1, 3)
    for (x, y, w, h) in objects:
        print(x, y, w, h)
        cv.rectangle(srcimg, (x, y), (x + w, y + h), (0, 0, 255), 4)
    return srcimg

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('./objdetect [image file] [cascade file]')
        sys.exit(-1)
    filename = sys.argv[1]
    cascadefilename = sys.argv[2]
    result = detect(filename, cascadefilename)
    cv.imwrite('box/detect.jpg', result)
    
    

