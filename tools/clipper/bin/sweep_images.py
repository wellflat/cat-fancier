#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import re
import sqlite3
import sys

def parsearguments():
    parser = argparse.ArgumentParser(description='sweep negative sample images from image directory')
    parser.add_argument('dbname', help='database name')
    parser.add_argument('targetdir', help='target directory')
    parser.add_argument('-n', '--dry', action='store_true', dest='dryrun', help='dry run mode')
    return parser.parse_args()
    
def sweepimages(dbname, targetdir, dryrun):
    if os.path.exists(dbname):
        db = sqlite3.connect(dbname)
        db.row_factory = sqlite3.Row
    else:
        print('not found %s' % (dbname,))
        sys.exit(-1)
    sql = 'SELECT filepath FROM samples WHERE status=100'
    cur = db.execute(sql)
    results = cur.fetchall()
    cur.close()
    totalcount = len(results)
    pattern = re.compile(targetdir)
    matchcount = 0
    for r in results:
        tgtfile = r['filepath']
        match = pattern.match(tgtfile)
        if match:
            matchcount += 1
            if dryrun:
                print('remove: %s' % (tgtfile,))
            else:
                os.remove(tgtfile)
                print('remove: %s ok' % (tgtfile,))
    db.close()
    print('total %s' % (totalcount,))
    print('remove %s ' % (matchcount,))
    print('complete.')

if __name__ == '__main__':
    args = parsearguments()
    dbname = args.dbname
    targetdir = args.targetdir
    dryrun = args.dryrun
    sweepimages(dbname, targetdir, dryrun)
