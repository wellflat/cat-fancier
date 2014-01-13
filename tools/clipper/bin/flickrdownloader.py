#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
from pprint import pprint

class FlickrClient(object):
    
    def __init__(self, apikey, apisecret, userid):
        self.__apikey = apikey
        self.__apisecret = apisecret
        self.__userid = userid
        self.__baseurl = 'http://api.flickr.com/services/rest/?method='

    def getuserid(self):
        return self.__userid
        
    def setuserid(self, userid):
        self.__userid = userid
        
    userid = property(getuserid, setuserid)
    
    def getbytag(self, tag, size='m'):
        url = self.__baseurl + 'flickr.photos.search&api_key=%s&user_id=%s&tags=%s&license=4&extras=url_%s&format=json&nojsoncallback=1' % (self.__apikey, self.__userid, tag, size)
        response = urllib2.urlopen(url)
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
            urls.append(p[key])
            
        return urls
            
if __name__ == '__main__':
    apikey = 'cf34b6d0fc8d5d2924ba67c7158739a3'
    apisecret = 'eca90abc0e259384'
    userid = '95962563@N02'
    flickr = FlickrClient(apikey, apisecret, userid)
    ret = flickr.getbytag('chocolat')
    #ret = flickr.getbytag('cat')
    total = ret['photos']['total']
    print('total photos: %s' % (total,))
    #flickr.downloadphotos(ret['photos']['photo'], '../static/tmp', verbose=True)
    print('complete.')
