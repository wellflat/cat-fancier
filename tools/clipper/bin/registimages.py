#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sqlite3

if __name__ == '__main__':
    dbname = 'samples.db'
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
        sql = 'INSERT INTO progress(pos, total) VALUES(0, ?)'
        db.execute(sql, (len(images),))
        db.commit()
    except sqlite3.IntegrityError as e:
        sql = 'UPDATE progress SET total=?'
        db.execute(sql, (len(images),))
        db.commit()
    db.close()
        
        
    

