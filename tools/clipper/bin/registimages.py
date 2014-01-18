#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import optparse
import os
import sqlite3

def createparser():
    parser = optparse.OptionParser()
    parser.add_option('-d', '--database', dest='dbname', default='samples.db')
    return parser

if __name__ == '__main__':
    parser = createparser()
    (options, args) = parser.parse_args()
    dbname = options.dbname
    db = sqlite3.connect(dbname)
    pattern = re.compile('.*[.](jpg|jpeg|png|bmp|gif)$')
    imagedir = os.path.join('static', 'images')
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
        sql = 'UPDATE progress SET total=?'
        db.execute(sql, (len(images),))
        db.commit()
    except sqlite3.IntegrityError as e:
        print(e)
    db.close()
        
        
    

