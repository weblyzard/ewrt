'''
Created on 21.06.2012

@author: Norman Suesstrunk

class for executing batch requests to the facebook api
'''
import unittest
import json
import urllib
import httplib
from itertools import chain

from eWRT.config import FACEBOOK_ACCESS_KEY
from eWRT.ws.facebook import FacebookWS

# TODO: check maximum BATCH_SIZE of 50 query per request

class FbBatchRequest(object):
    '''
    @class FacebookBatchRequest
    Class for sending batch requests to the facebook api
    the actual requests are constructed with objects from the FacebookWS class.  
    '''

    def __init__(self, access_token=FACEBOOK_ACCESS_KEY):
        '''
        Constructor
        '''
        self.fbWSList = [] # stores a list of FacebookWS-objects
        self.batchHTTPParam = 'batch' # http post parameter for the facebook batch http interface
        self.accessTokenHTTPParam = 'access_token'
        self.faceBookGraphHost = 'graph.facebook.com'
        self.access_token = access_token
    
    def run_search(self, terms, objectType='all', since=None, limit=None):
        ''' runs a batch search '''
        if not isinstance(terms, list):
            terms = [terms]
            
        for term in terms: 
            self.fbWSList.append(FacebookWS(term, objectType, since, limit))
    
        return self.do_batch_search()
    
    def get_path(self, paths, since=None, limit=None):
        if not isinstance(paths, list):
            paths = [paths]
        
        for path in paths: 
            self.fbWSList.append(FacebookWS(path, 'path', since, limit))
        
        return self.do_batch_search()
    
    def add_facebook_ws(self, faceBookWS):
        '''
        add a FacebookWS-Object to the batch
        '''
        self.fbWSList.append(faceBookWS)
    
    def _get_json_batch_request_string(self):
        '''
        delivers the json-string in the apropriate format for the facebook batch api
        '''
        result = list(chain(* [ fbWebservice.getJsonListStructure() 
                                    for fbWebservice in self.fbWSList ]))
        return json.dumps(result)

    
    def _make_request_params(self):
        '''
        constructs a dictionary with all the necessary http params and their values
        '''
        urlargs = {}
        urlargs[self.accessTokenHTTPParam] = self.access_token
        urlargs[self.batchHTTPParam] = self._get_json_batch_request_string()
        print urlargs
        return urlargs
    
    def _send_post(self):
        '''
        sends the batch request as post to the facebook batch request api
        returns all the search results for the batch request
        '''
        params = urllib.urlencode(self._make_request_params())
        
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPSConnection(self.faceBookGraphHost)
        conn.request("POST", "/", params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
        return json.loads(data)
    
    def do_batch_search(self):
        '''
        executes the batch request to the facebook api
        '''
        result = []
        json_search_result = self._send_post()
        
        if 'error' in json_search_result:
            raise Exception(json_search_result['error']['message'])
        
        for row in json_search_result: 
            print row['body']
            for post in json.loads(row['body'])['data']:
                result.append(post)
                url = 'http://www.facebook.com/%s' % post['id'].replace('_', '/posts/')
                if 'comments' in post and 'data' in post['comments']:
                    for comment in post['comments']['data']:
                        comment['type'] = 'comment'
                        comment['parent_url'] = url
                        comment['url'] = url
                        result.append(comment)
            
        return result
        
class TestFacebookWS(unittest.TestCase):
    
    def setUp(self):
        from datetime import datetime
        self.fbBatchRequest = FbBatchRequest()
        fbWS1 = FacebookWS('Linus Torvalds', 'post', since=datetime(2012, 07, 01))
        self.fbBatchRequest.add_facebook_ws(fbWS1)
        fbWS2 = FacebookWS('Linus Torvalds')
        self.fbBatchRequest.add_facebook_ws(fbWS2)
        fbWS3 = FacebookWS('Heinz Lang', 'user')
        self.fbBatchRequest.add_facebook_ws(fbWS3)
        
    def test_get_json_batch_request_string(self):
        json_string = self.fbBatchRequest._get_json_batch_request_string()
        assert len(json.loads(json_string)) == 7
        
        # The order of the requests always changes
        # assert json == '[{"method": "GET", "relative_url": "/search?q=Linus+Torvalds&since=1341093600.0&type=post"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=post"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=user"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=page"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=event"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=group"}, {"method": "GET", "relative_url": "/search?q=Heinz+Lang&type=user"}]' 
        
    def test_batch_search(self):
        searchResult = self.fbBatchRequest.do_batch_search()
        self.assertFalse('error' in searchResult)
        assert len(searchResult) > 0        
    
    def test_bad_request(self):
        access_token = "AAAElj9ZBZCquoBAGkKlcPvJsUCpyAZBxz6nsOYr8LAmpIj9Q9EZCKl9xVAYmlXGh2UQvhVellSWsZALPn6V73ZAZBiaxlwqkWlUjGVLzAHd7gZDZD"
        fbBatchRequest = FbBatchRequest(access_token)
        
        try: 
            fbBatchRequest.run_search('Linus Torvalds')
        except Exception, e: 
            print 'thats ok: %s' % e
            assert True
    
    def test_batch_search2(self):
        fbBatchRequest = FbBatchRequest()
        result = fbBatchRequest.run_search(['Wien'], 'post', 100)
        assert len(result) > 0
    
    def test_feed_mirroring(self):
        fbBatchRequest = FbBatchRequest()
        result = fbBatchRequest.get_path('58220918250/feed', limit=1)
        
        for x in result:
            print x
        assert len(result) >= 1
    
if __name__ == "__main__":

    unittest.main()
