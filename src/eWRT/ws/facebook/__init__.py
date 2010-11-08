#!/usr/bin/env python
import logging, json, sys, unittest, urllib
from eWRT.config import FACEBOOK_ACCESS_KEY
from eWRT.lib import Webservice, Result 
from eWRT.lib.ResultSet import ResultSet
from eWRT.access.http import Retrieve
from urllib2 import HTTPError

class FacebookWS(object):
    """ class for fetching and storing the data of a user
    requires that the facebook API key and the facebook secret key are
    set in the configuration file. These can be retrieved from facebook
    """
    FB_OBJECT_TYPES = ['post', 'user', 'page', 'event', 'group']

    def __init__(self):
        """ init """       
        self.retrieve = Retrieve('facebookWS')


    def search(self, term, objectType='all'):
        '''
        searches for the given term 
        @param term: term to search
        @param objectType: objectType to search in (post, user, page, event, group)
        @return: search result
        '''
        args = {}
        result= []
        
        args['q'] = term
        
        if objectType in self.FB_OBJECT_TYPES:
            args['type'] = objectType
            result = self.makeRequest('search', args)
        else:
            
            # search all object types
            for type in self.FB_OBJECT_TYPES:
                args['type'] = type
                result.extend(self.makeRequest('search', args))

        return result


    def makeRequest(self, path, args={}):
        '''
        makes a request to the graph API
        @param path: path to query
            e.g. userprofile of current user: me
                 feed of user/group/page 122222: 122222/feed
        @return: fetched data
        '''
        
        if not args.has_key('access_token'):
            args['access_token'] = FACEBOOK_ACCESS_KEY
        
        url = "https://graph.facebook.com/%s?%s" % (path, urllib.urlencode(args)) 
        
        return self.requestURL(url)


    def requestURL(self, url):
        '''
        fetches the data for the give URL from the graph API
        @param url: valid graph-api-url
        @return: fetched data 
        '''
        
        result = []
        
        try:
        
            file = self.retrieve.open(url)
            fetched = json.loads(file.read())
            
            
            logging.debug('processing url %s' % url)
            
            if fetched.has_key('data'):
                
                # process paging
                if fetched.has_key('paging'):
                    if fetched['paging'].has_key('previous'):
                        result.extend(self.requestURL(fetched['paging']['next']))
                        print 'After processing paging', len(result)
                result.extend(fetched['data'])
                print 'After adding data', len(result)
                print result
            else:
                # profiles for example don't contain a data dictionary
                result.append(fetched)
                print 'After appending fetched', len(result)
        
        except HTTPError:
            print 'Error: Bad Request for url', url
        
        return result

class TestFacebookWS(unittest.TestCase):

    def setUp(self):
        ''' setup the webservice '''
        self.fb = FacebookWS()
        
    def testSearch(self):
        ''' tests the search '''
        resultPage = self.fb.search('Linus Torvalds', 'page')
        assert len(resultPage) > 5
        assert resultPage[0]['name'] == 'Linus Torvalds'

        resultAll = self.fb.search('Linus Torvalds')
        assert len(resultAll) > len(resultPage)

        result = self.fb.search('Heinz Lang', 'user')
        assert len(result) > 5

    def testFetchingProfile(self):
        ''' tests fetching the profile '''
        result = self.fb.makeRequest('me')
        assert len(result) == 1
        assert result[0].has_key('first_name')

    def testRequestUrl(self):
        ''' tests request url '''
        url = 'https://graph.facebook.com/me?access_token=%s' % FACEBOOK_ACCESS_KEY
        result = self.fb.requestURL(url)
        assert len(result) == 1
        assert result[0].has_key('first_name')
        
    def testBadRequest(self):
        ''' tests that a bad request won't disturb the program'''

        # this URL contains an invalid access token
        url = 'https://graph.facebook.com/me?access_token=2227470867%7C2._jNijjNpTLF_OrmDqYTEA__.3600.1288695600-1145817399%7CECkapj6t0eZK8DjnNfSVRANS8lI'
        result = self.fb.requestURL(url)
        assert [] == result
        

    def testFetchingPaging(self):
        ''' tests if the results are correctly fetched '''
        param = {'path': '1145817399/feed', 'args': {}}
        result = self.fb.makeRequest(param['path'], param['args'])
        assert result

if __name__ == "__main__":

    unittest.main()

