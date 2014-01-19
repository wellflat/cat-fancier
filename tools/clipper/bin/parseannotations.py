#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import re
from xml.etree import ElementTree

if __name__ == '__main__':
    f = open('annotation.dat', 'wb')
    pattern = re.compile('.*[.](xml)$')
    xmldir = '../static/oxford/annotations/xmls'
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
