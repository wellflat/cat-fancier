#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import re
import shutil
from xml.etree import ElementTree

## ll | egrep 'Abyssinian|Bengal|Birman|Bombay|British|Egyptian|Main|Persian|Ragdoll|Russian|Siamese|Sphynx' | wc -l''

def removedogimages():
    imagedir = 'static/oxford/images'
    pattern = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
    images = [image for image in os.listdir(imagedir) if re.match(pattern, image)]
    for i, imagefile in enumerate(images):
        if imagefile[0].islower():
            imagesrc = os.path.join(imagedir, imagefile)
            os.remove(imagesrc)

def removedogxmls():
    xmldir = 'static/oxford/annotations/xmls'
    pattern = re.compile('.*[.](xml)$')
    xmls = [xml for xml in os.listdir(xmldir) if re.match(pattern, xml)]
    for i, xml in enumerate(xmls):
        if xmls[i][0].islower():
            xmlsrc = os.path.join(xmldir, xmls[i])
            #print(xmlsrc)
            os.remove(xmlsrc)

def createannotationfile():
    f = open('annotation.dat', 'wb')
    pattern = re.compile('.*[.](xml)$')
    xmldir = 'static/oxford/annotations/xmls'
    imgdir = 'static/oxford/images/'
    xmls = [xml for xml in os.listdir(xmldir) if re.match(pattern, xml)]
    annotationdata = ''
    for i, xml in enumerate(xmls):
        xmlsrc = os.path.join(xmldir, xmls[i])
        tree = ElementTree.parse(xmlsrc)
        elem = tree.getroot()
        filename = elem.find('.//filename').text
        if filename[0].isupper():
            #print(filename)
            xmin = elem.find('.//xmin').text
            ymin = elem.find('.//ymin').text
            xmax = elem.find('.//xmax').text
            ymax = elem.find('.//ymax').text
            width = int(xmax) - int(xmin)
            height = int(ymax) - int(ymin)
            #print(xmin,ymin,xmax,ymax)
            imgsrc = imgdir + filename
            annotationdata += "%s 1 %d %d %d %d\n" % (imgsrc, int(xmin), int(ymin), width, height)
    f.write(annotationdata)
    f.close()

if __name__ == '__main__':
    #createannotationfile()
    #removedogimages()
    removedogxmls()
    
