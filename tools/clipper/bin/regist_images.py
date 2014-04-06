#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import re
import os
import sqlite3
import sys

def parsearguments():
    parser = argparse.ArgumentParser(description='regist images to sqlite3 database')
    parser.add_argument('dbname')
    return parser.parse_args()

def registimages(dbname, imagedir):
    if os.path.exists(dbname):
        db = sqlite3.connect(dbname)
    else:
        print('not found %s' % (dbname,))
        sys.exit(-1)
    pattern = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
    images = [image for image in os.listdir(imagedir) if re.match(pattern, image)]
    sql = 'INSERT INTO samples(filepath, status) VALUES(?, ?)'
    for i, image in enumerate(images):
        try:
            imagesrc = os.path.join(imagedir, images[i])
            print(imagesrc)
            db.execute(sql, (imagesrc, 100))
        except sqlite3.IntegrityError as e:
            pass
    db.commit()
    try:
        sql = 'UPDATE progress SET total=(SELECT COUNT(id) FROM samples)'
        db.execute(sql)
        db.commit()
    except sqlite3.IntegrityError as e:
        db.rollback()
        print(e)
    db.close()

if __name__ == '__main__':
    args = parsearguments()
    dbname = args.dbname
    imagedir = 'static/images/catdata/CAT_02'
    registimages(dbname, imagedir)
        
        
    

