#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import re
import os
import sqlite3
from pprint import pprint

def parsearguments():
    parser = argparse.ArgumentParser(description='creates annotation data')
    parser.add_argument('dbname', help='database name')
    parser.add_argument('-p', '--positive', dest='positivefilename',
                        default='positive.dat')
    parser.add_argument('-n', '--negative', dest='negativefilename',
                        default='negative.dat')
    return parser.parse_args()
    
def connectdb(dbname):
    if os.path.exists(dbname):
        db = sqlite3.connect(dbname)
        db.row_factory = sqlite3.Row
    else:
        print('cannnot open %s' % (dbname,))
        return None
    return db

def createannotations(db):
    annotationdata = ''
    sql = 'SELECT filepath, x, y, width, height FROM samples WHERE status=200'
    try:
        rv = db.execute(sql)
        for r in rv:
            annotationdata += "%s 1 %d %d %d %d\n" % (r['filepath'], r['x'], r['y'], r['width'], r['height'])
        print(annotationdata)
    except sqlite3.OperationalError as e:
        print(e)
        return None
    return annotationdata

def createnegativefilelist(db):
    negativefilelist = ''
    sql = 'SELECT filepath FROM samples WHERE status=100'
    try:
        rv = db.execute(sql)
        for r in rv:
            negativefilelist += "%s\n" % (r['filepath'],)
        print(negativefilelist)
    except sqlite3.OperationalError as e:
        print(e)
        return None
    return negativefilelist

def appendnegativefilelist(dirpath, dirname):
    pattern = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
    imagedir = os.path.join(dirpath, dirname)
    images = [image for image in os.listdir(imagedir) if re.match(pattern, image)]
    negativefilelist = ''
    for i, image in enumerate(images):
        imagesrc = os.path.join(imagedir, images[i])
        negativefilelist += "%s\n" % (imagesrc,)
    return negativefilelist

if __name__ == '__main__':
    args = parsearguments()
    dbname = args.dbname
    db = connectdb(dbname)
    positivefile = open(args.positivefilename, 'wb')
    negativefile = open(args.negativefilename, 'wb')
    annotationdata = createannotations(db)
    
    if annotationdata:
        positivefile.write(annotationdata)
    positivefile.close()
    
    #negativefilelist = createnegativefilelist(db)
    negativefilelist = appendnegativefilelist('static/negative/images', 'other')

    if negativefilelist:
        negativefile.write(negativefilelist)
    negativefile.close()

    db.close()
