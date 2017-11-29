#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from eWRT.config import FACEBOOK_ACCESS_KEY
from eWRT.ws.facebook import FacebookWS


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
        assert 'first_name' in result[0]

    def testRequestUrl(self):
        ''' tests request url '''
        url = 'https://graph.facebook.com/me?access_token=%s' % FACEBOOK_ACCESS_KEY
        result = self.fb._requestURL(url)
        assert len(result) == 1
        assert 'first_name' in result[0]

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

