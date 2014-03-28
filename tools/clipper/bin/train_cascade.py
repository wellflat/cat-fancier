#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
import time
from pprint import pprint


def parsearguments():
    parser = argparse.ArgumentParser(description='run cascade training')
    parser.add_argument('positivefilename', help='positive sample file')
    parser.add_argument('negativefilename', help='negative sample file')
    parser.add_argument('-f', '--maxfarate', help='max false alarm rate', type=float, default=0.5)
    return parser.parse_args()

def createsamples(positivefile, vecdir='./vec'):
    os.environ['PATH'] = '/bin:/usr/bin:/usr/local/bin'
    if not os.path.isdir(vecdir):
        os.mkdir(vecdir)
    numpos = len(open(positivefile).readlines())
    print('samples: %d' % (numpos,))
    vecfile = vecdir + '/' + positivefile + '.vec'
    cmdline = ['opencv_createsamples', '-info', positivefile,
               '-vec', vecfile, '-num', str(numpos)]
    print(' '.join(cmdline))
    try:
        p = subprocess.Popen(cmdline, cwd='./', shell=False,
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

    return (vecfile, numpos)

def traincascade(vecfile, numpos, negativefilename, maxfarate=0.5):
    numneg = len(open(negativefile).readlines())
    numpos = numpos*0.85
    cmdline = [
        'opencv_traincascade', '-data', dstdir, '-vec', vecfile,
        '-bg', bgfile, '-numPos', str(numpos), '-numNeg', str(numneg),
        '-featureType', 'LBP', '-maxFalseAlarmRate', str(maxfarate)
    ]
    try:
        p = subprocess.Popen(cmdline, cwd='./', shell=False,
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


if __name__ == '__main__':
    args = parsearguments()
    positivefilename = args.positivefilename
    negativefilename = args.negativefilename
    maxfarate = args.maxfarate
    (vecfile, numpos) = createsamples(positivefilename)
    print(vecfile, numpos, negativefilename, maxfarate)
    
    
