#!/usr/bin/env python
# coding: UTF-8
"""
@package eWRT.ws.facebook
Access to the Facebook API.
"""

import logging, json, sys, unittest, urllib

from urllib2 import HTTPError, URLError

from eWRT.config import FACEBOOK_ACCESS_KEY

# facebook
FACEBOOK_API_KEY = "322774841141994"
FACEBOOK_SECRET_KEY = "b07f413baf9650d2363f1c8813ece6da"
FACEBOOK_ACCESS_KEY = "AAAElj9ZBZCquoBANxb2ot9Trt7vA5WEH6X4JX1Pyxl0d2tGxjPjZBP3DGs7Rgh6vuuBx5vCHRfCG15sQThQJRZB0ylXHgQ4x6Cptq2B6BgZDZD"
# FACEBOOK_SESSION_KEY = "session-key"

from eWRT.lib import Webservice, Result
from eWRT.lib.ResultSet import ResultSet
from eWRT.access.http import Retrieve

class FacebookWS(object):
    """ 
    @class FacebookWS
    class for fetching and storing the data of a user
    requires that the facebook API key and the facebook secret key are
    set in the configuration file. These can be retrieved from facebook
    """
    FB_OBJECT_TYPES = ['post', 'user', 'page', 'event', 'group']
    
    
    # added: class properties for storing searchTerm and searchType

    def __init__(self, term="", objectType='all'):
        """ init """
        self.retrieve = Retrieve('facebookWS')
        self.term = term
        self.objectType = 'all'

    def search(self, term, objectType="all"):
        '''
        searches for the given term 
        @param term: term to search
        @param objectType: objectType to search in (post, user, page, event, group)
        @return: search result
        '''
        self.term = term
        self.objectTyp = objectType
        args = {}
        result = []

        args['q'] = self.term

        if self.objectType in self.FB_OBJECT_TYPES:
            args['type'] = self.objectType
            result = self.makeRequest('search', args)
        elif self.objectType == 'all':
            # search all object types
            for obj_type in self.FB_OBJECT_TYPES:
                args['type'] = obj_type
                result.extend(self.makeRequest('search', args))
        else:
            raise ValueError, 'Illegal Object type %s' % (self.objectType)

        return result


    def makeRequest(self, path, args={}, maxDoc=None):
        '''
        makes a request to the graph API
        @param path: path to query, e.g. feed of user/group/page 122222: 122222/feed
        @return: fetched data
        '''

        if not args.has_key('access_token'):
            # args['access_token'] = "b07f413baf9650d2363f1c8813ece6da" #very unflexible, its hardcoded...
            args['access_token'] = FACEBOOK_ACCESS_KEY

        url = "https://graph.facebook.com/%s?%s" % (path, urllib.urlencode(args))
        result = self._requestURL(url, maxDoc)
        print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&'
        print result
        return result
    
    def getJsonListStructure(self):
        jsonListStructure = []
        args = {}
        args['q'] = self.term
        if self.objectType in self.FB_OBJECT_TYPES:
            args['type'] = self.objectType
            jsonListStructure.append({'method': "GET", 
                                      "relative_url" : "/search?"+urllib.urlencode(args)});
        elif self.objectType == 'all':
            for obj_type in self.FB_OBJECT_TYPES:
                args['type'] = obj_type
                jsonListStructure.append({'method': "GET", 
                                          "relative_url" : "/search?"+urllib.urlencode(args)});
        return jsonListStructure
                

    def _requestURL(self, url, maxDoc=None, result=None, tried=None):
        '''
        fetches the data for the give URL from the graph API
        @param url: valid graph-api-url
        @return: fetched data 
        '''

        if result == None:
            result = []
        if maxDoc == None:
            maxDoc = 1000
        if tried == None:
            tried = False

        try:

            f = self.retrieve.open(url)
            fetched = json.loads(f.read())

            logging.debug('processing url %s' % url)

            if isinstance(fetched, dict):

                if fetched.has_key('data'):
                    result.extend(fetched['data'])

                    # process paging
                    if len(result) < maxDoc:
                        if fetched.has_key('paging') and fetched['paging'].has_key('previous'):
                            result = (self._requestURL(fetched['paging']['previous'],
                                                      maxDoc, result))
                            print 'After processing paging', len(result)

                else:
                    # profiles for example don't contain a data dictionary
                    result.append(fetched)
                    print 'After appending fetched', len(result)

        except HTTPError:
            print 'Error: Bad Request for url', url
            if not tried:
                result = self._requestURL(url, maxDoc, result, True)
        except URLError:
            print 'URLError', url
            if not tried:
                result = self._requestURL(url, maxDoc, result, True)

        return result


class TestFacebookWS(unittest.TestCase):

    def setUp(self):
        ''' setup the webservice '''
        self.fb = FacebookWS()

    def testSearch(self):
        ''' tests the search '''
        resultPage = self.fb.search('Linus Torvalds', 'page')
        print resultPage
        assert len(resultPage) > 5

        resultAll = self.fb.search('Linus Torvalds')
        print resultAll
        assert len(resultAll) > len(resultPage)

        result = self.fb.search('Heinz Lang', 'user')
        print result
        assert len(result) > 5

    def testFetchingProfile(self):
        ''' tests fetching the profile '''
        result = self.fb.makeRequest('me')
        assert len(result) == 1
        assert result[0].has_key('first_name')

    def testRequestUrl(self):
        ''' tests request url '''
        url = 'https://graph.facebook.com/me?access_token=%s' % FACEBOOK_ACCESS_KEY
        result = self.fb._requestURL(url)
        assert len(result) == 1
        assert result[0].has_key('first_name')

    def testBadRequest(self):
        ''' tests that a bad request won't disturb the program'''

        # this URL contains an invalid access token
        url = 'https://graph.facebook.com/me?access_token=2227470867%7C2._jNijjNpTLF_OrmDqYTEA__.3600.1288695600-1145817399%7CECkapj6t0eZK8DjnNfSVRANS8lI'
        result = self.fb._requestURL(url)
        assert [] == result

    def testFetchingPaging(self):
        ''' tests if the results are correctly fetched '''
        param = {'path': '358298686286/feed', 'args': {}}
        result = self.fb.makeRequest(param['path'], param['args'])
        assert result

    def testMakeSearchRequest(self):
        '''Tests searching by making a request'''
        args = {'limit':20, 'type':'post', 'q':'bildung'}
        result = self.fb.makeRequest('search', args)
        print result

    def testBooleanReturn(self):
        args = {}
        result = self.fb.makeRequest('1450854928_205387146163105', args)
        print result

if __name__ == "__main__":

    unittest.main()

