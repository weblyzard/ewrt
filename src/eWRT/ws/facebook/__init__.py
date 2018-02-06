#!/usr/bin/env python
# coding: UTF-8
"""
@package eWRT.ws.facebook
Access to the Facebook API.
"""
import time
import logging
import json
import sys
import unittest
import urllib

from urllib2 import HTTPError, URLError

from eWRT.lib import Webservice, Result
from eWRT.lib.ResultSet import ResultSet
from eWRT.access.http import Retrieve
from eWRT.config import FACEBOOK_ACCESS_KEY

logging.getLogger(__name__)


class FacebookWS(object):
    """ 
    @class FacebookWS
    class for fetching and storing the data of a user
    requires that the facebook API key and the facebook secret key are
    set in the configuration file. These can be retrieved from facebook
    """
    FB_OBJECT_TYPES = ['post', 'user', 'page', 'event', 'group', 'path']

    # Expires July 8, 2017
    # 9https://developers.facebook.com/docs/apps/changelog)
    GRAPH_API_VERSION = 'v2.3'

    retrieve = Retrieve('facebookWS')
    # added: class properties for storing searchTerm and searchType

    def __init__(self, term=None, objectType='all', since=None, limit=None):
        """ init """
        self.term = term

        if objectType == 'all':
            objectType = 'post'

        self.objectType = objectType

        if since and not isinstance(since, int):
            since = time.mktime(since.timetuple())

        self.since = since
        self.limit = limit

    @classmethod
    def search(cls, term, objectType="all"):
        '''
        searches for the given term 
        @param term: term to search
        @param objectType: objectType to search in (post, user, page, event, group)
        @return: search result
        '''
        args = {}
        result = []

        args['q'] = term

        if objectType in cls.FB_OBJECT_TYPES:
            args['type'] = objectType
            result = cls.makeRequest('search', args)
        elif objectType == 'all':
            # search all object types
            for obj_type in cls.FB_OBJECT_TYPES:
                args['type'] = obj_type
                result.extend(cls.makeRequest('search', args))
        else:
            raise ValueError, 'Illegal Object type %s' % (objectType)

        return result

    @classmethod
    def makeRequest(cls, path, args={}, maxDoc=None, method='get'):
        '''
        makes a request to the graph API
        @param path: path to query, e.g. feed of user/group/page 122222: 122222/feed
        @return: fetched data
        '''

        if not 'access_token' in args:
            # args['access_token'] = "b07f413baf9650d2363f1c8813ece6da" #very
            # unflexible, its hardcoded...
            args['access_token'] = FACEBOOK_ACCESS_KEY

        if method == 'post':
            args['method'] = 'POST'

        url = "https://graph.facebook.com/%s?%s" % (
            path, urllib.urlencode(args))
        result = cls._requestURL(url, maxDoc)
        return result

    def getJsonListStructure(self):
        request = None
        args = {}
        args['q'] = self.term

        if isinstance(args['q'], unicode):
            args['q'] = args['q'].encode('utf-8')

        if self.since:
            args['since'] = int(self.since)

        if self.limit:
            args['limit'] = self.limit

        if self.objectType == 'path':
            args_string = ''

            if 'q' in args:
                del args['q']

            if len(args):
                args_string = '?%s' % urllib.urlencode(args)

            request = {'method': "GET",
                       "relative_url": '%s/%s%s' % (self.GRAPH_API_VERSION,
                                                    self.term, args_string)}

        elif self.objectType in self.FB_OBJECT_TYPES:
            args['type'] = self.objectType
            request = {'method': "GET",
                       "relative_url": "/search?%s" % urllib.urlencode(args)}

        elif self.objectType == 'all':
            for obj_type in self.FB_OBJECT_TYPES:
                if obj_type == 'path':
                    continue
                args['type'] = obj_type
                request = {'method': "GET",
                           "relative_url": "/search?" + urllib.urlencode(args)}

        return request

    @classmethod
    def _requestURL(cls, url, maxDoc=None, result=None, tried=None):
        '''
        fetches the data for the give URL from the graph API
        @param url: valid graph-api-url
        @return: fetched data 
        '''

        if not result:
            result = []
        if not maxDoc:
            maxDoc = 1000
        if not tried:
            tried = False

        try:

            f = cls.retrieve.open(url)
            fetched = json.loads(f.read())
            tried = True
            logging.debug('processing url %s' % url)

            if isinstance(fetched, dict):

                if 'data' in fetched:
                    if not len(fetched['data']):
                        return result

                    result.extend(fetched['data'])

                    # process paging
                    if len(result) < maxDoc:
                        if 'paging' in fetched and 'previous' in fetched['paging']:
                            result = (cls._requestURL(fetched['paging']['previous'],
                                                      maxDoc, result))
                            print 'After processing paging', len(result)

                else:
                    # profiles for example don't contain a data dictionary
                    result.append(fetched)
                    print 'After appending fetched', len(result)

        except HTTPError, e:
            print 'Error: Bad Request for url %s: %s' % (url, e)
            if not tried:
                result = cls._requestURL(url, maxDoc, result, True)
        except URLError, e:
            print 'URLError for url %s: %s' % (url, e)
            if not tried:
                result = cls._requestURL(url, maxDoc, result, True)

        return result
