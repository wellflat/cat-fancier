#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import sqlite3
import sys
from pprint import pprint

import numpy as np

def connectdb(dbname):
    if os.path.exists(dbname):
        db = sqlite3.connect(dbname)
        db.row_factory = sqlite3.Row
    else:
        print('cannnot open %s' % (dbname,))
        return None
    return db
    
def calcratio(db):
    try:
        sql = 'SELECT width, height FROM samples WHERE status=200'
        rv = db.execute(sql)
        ratio = []
        for r in rv:
            ratio.append(float(r['width'])/float(r['height']))
        arr = np.array(ratio)
        print(np.mean(arr),np.amax(arr),np.amin(arr),np.median(arr))
    except sqlite3.OperationalError as e:
        print(e)
        sys.exit(-1)


if __name__ == '__main__':
    dbname = 'db/samples.db'
    db = connectdb(dbname)
    calcratio(db)
