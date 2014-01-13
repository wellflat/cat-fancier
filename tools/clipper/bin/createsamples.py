#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from pprint import pprint

if __name__ == '__main__':
    dbname = 'samples.db'
    db = sqlite3.connect(dbname)
    db.row_factory = sqlite3.Row
    positivefile = open('positive.dat', 'wb')
    negativefile = open('negative.dat', 'wb')
    positivestr = ''
    negativestr = ''
    sql = 'SELECT filepath, x, y, width, height FROM samples WHERE status=200'
    rv = db.execute(sql)
    for r in rv:
        positivestr += "%s 1 %d %d %d %d\n" % (r['filepath'], r['x'], r['y'], r['width'], r['height'])
    print(positivestr)
    positivefile.write(positivestr)
    positivefile.close()

    sql = 'SELECT filepath FROM samples WHERE status=100'
    rv = db.execute(sql)
    for r in rv:
        negativestr += "%s\n" % (r['filepath'],)
    print(negativestr)
    negativefile.write(negativestr)
    negativefile.close()
    
    
    
    
