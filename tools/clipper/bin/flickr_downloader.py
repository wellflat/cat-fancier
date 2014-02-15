#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import urllib2
import json
import sys
from pprint import pprint

def parsearguments():
    parser = argparse.ArgumentParser(description='image downloader from flickr')
    parser.add_argument('-d', '--download', action='store_true', dest='download')
    parser.add_argument('-t', '--tag', dest='tag')
    parser.add_argument('-p', '--page', dest='maxpage', type=int, default=10)
    parser.add_argument('-c', '--cconly', action='store_true', dest='cconly', default=False)
    parser.add_argument('-m', '--mine', action='store_true', dest='mine', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False)
    return parser.parse_args()

class FlickrClient(object):
    
    def __init__(self, apikey, apisecret, userid):
        self.__apikey = apikey
        self.__apisecret = apisecret
        self.__userid = userid
        self.__baseurl = u'http://api.flickr.com/services/rest/?method='

    def getuserid(self):
        return self.__userid
        
    def setuserid(self, userid):
        self.__userid = userid
        
    userid = property(getuserid, setuserid)
    
    def getbytag(self, tag, page=1, ismine=True, cconly=True, size='m'):
        url = self.__baseurl + u'flickr.photos.search&api_key=%s&tags=%s&extras=url_%s&page=%s&format=json&nojsoncallback=1' % (self.__apikey, tag, size, page)
        if ismine:
            url += '&user_id=%s' % (self.__userid,)
        if cconly:
            url += '&license=4'
        response = urllib2.urlopen(url.encode('utf-8'))
        parsed = json.loads(response.read())
        return parsed

    def downloadphotos(self, photolist, targetdir, size='m', verbose=False):
        urls = self.__buildphotourls(photolist, size=size)    
        for url in urls:
            if verbose:
                print('download: %s' % (url,))
                
            response = urllib2.urlopen(url)
            f = open(targetdir + '/' + url.split('/')[-1], 'wb')
            f.write(response.read())
            f.close()
            
    def __buildphotourls(self, photolist, size='m'):
        urls = []
        key = 'url_%s' % (size,)
        for p in photolist:
            try:
                urls.append(p[key])
            except KeyError as e:
                pass
            
        return urls
            
if __name__ == '__main__':
    try:
        args = parsearguments()
        apikey = 'cf34b6d0fc8d5d2924ba67c7158739a3'
        apisecret = 'eca90abc0e259384'
        userid = '95962563@N02'
        flickr = FlickrClient(apikey, apisecret, userid)
        if args.tag:
            fsencoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
            tag = args.tag.decode(fsencoding)
        else:
            tag = u'cat'
        print('search by %s' % (tag,))
        print('creative commons only: %s' % (args.cconly,))
        print('my photo only: %s' % (args.mine,))
        dstdir = './static/images/tmp'
        print('save to: %s' % (dstdir,))
        ret = flickr.getbytag(tag, ismine=args.mine, cconly=args.cconly)
        pagenum = int(ret['photos']['pages'])
        if pagenum > args.maxpage:
            pagenum = args.maxpage
        print('total pages: %s' % (pagenum,))
        total = ret['photos']['total']
        print('total photos: %s' % (total,))
        firstpage = 1
        for i in xrange(firstpage, pagenum + 1):
            print('page %s' % (i,))
            ret = flickr.getbytag(tag, page=i, ismine=args.mine, cconly=args.cconly)
            if args.download:
                flickr.downloadphotos(ret['photos']['photo'], dstdir, verbose=True)
            
        print('complete.')
    except KeyboardInterrupt as e:
        print('Keyborad Interrupt')
        sys.exit(-1)
