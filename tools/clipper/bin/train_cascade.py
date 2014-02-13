#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import optparse
import os
import subprocess
import sys
import time
from pprint import pprint

def createparser():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--positive', dest='positivefilename',
                      default='positive.dat')
    return parser

def countline(filename):
    return len(open(filename).readlines())

def createsamples(positivefile):
    os.environ['PATH'] = '/bin:/usr/bin:/usr/local/bin'
    cwd = './'
    vecdir = cwd + 'vec/'
    if not os.path.isdir(vecdir):
        os.mkdir(vecdir)
    linecount = countline(positivefile)
    cmdline = ['opencv_createsamples', '-info', positivefile,
               '-vec', vecdir + positivefile + '.vec',
               '-num', str(linecount)]
    try:
        p = subprocess.Popen(cmdline, cwd=cwd, shell=False,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, close_fds=True)
    except OSError as e:
        print(e)
        sys.exit(-1)
    
    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(line.rstrip())
    ret = p.wait()
    print('ret: %d' % (ret,))

def traincascade():
    pass

if __name__ == '__main__':
    parser = createparser()
    (options, args) = parser.parse_args()
    positivefilename = options.positivefilename
    createsamples(positivefilename)
