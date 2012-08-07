'''
Created on 21.06.2012

@author: Norman Suesstrunk

class for executing batch requests to the facebook api
'''
import unittest
from eWRT.ws.facebook import FacebookWS
import json
import urllib
import httplib
from itertools import chain

class FbBatchRequest(object):
    '''
    @class FacebookBatchRequest
    Class for sending batch requests to the facebook api
    the actual requests are constructed with objects from the FacebookWS class.  
    '''

    def __init__(self, access_token):
        '''
        Constructor
        '''
        self.fbWSList = [] # stores a list of FacebookWS-objects
        self.batchHTTPParam = 'batch' # http post parameter for the facebook batch http interface
        self.accessTokenHTTPParam = 'access_token'
        self.faceBookGraphHost = 'graph.facebook.com'
        self.access_token = access_token
        
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
        return self._send_post(); 
        
class TestFacebookWS(unittest.TestCase):
    def setUp(self):
        self.access_token = "AAAElj9ZBZCquoBAGkKlcPvJsUCpyAZBxz6nsOYr8LAmpIj9Q9EZCKl9xVAYmlXGh2UQvhVellSWsZALPn6V73ZAZBiaxlwqkWlUjGVLzAHd7gZDZD"
        self.fbBatchRequest = FbBatchRequest(self.access_token)
        
        fbWS1 = FacebookWS('Linus Torvalds', 'page')
        self.fbBatchRequest.add_facebook_ws(fbWS1)
        fbWS2 = FacebookWS('Linus Torvalds')
        self.fbBatchRequest.add_facebook_ws(fbWS2)
        fbWS3 = FacebookWS('Heinz Lang', 'user')
        self.fbBatchRequest.add_facebook_ws(fbWS3)
        
    def test_get_json_batch_request_string(self):
        json = self.fbBatchRequest._get_json_batch_request_string()
        assert json == '[{"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=post"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=user"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=page"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=event"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=group"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=post"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=user"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=page"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=event"}, {"method": "GET", "relative_url": "/search?q=Linus+Torvalds&type=group"}, {"method": "GET", "relative_url": "/search?q=Heinz+Lang&type=post"}, {"method": "GET", "relative_url": "/search?q=Heinz+Lang&type=user"}, {"method": "GET", "relative_url": "/search?q=Heinz+Lang&type=page"}, {"method": "GET", "relative_url": "/search?q=Heinz+Lang&type=event"}, {"method": "GET", "relative_url": "/search?q=Heinz+Lang&type=group"}]' 
        
    def test_batch_search(self):
        searchResult = self.fbBatchRequest.do_batch_search()
        assert len(searchResult)!=0        
        
if __name__ == "__main__":

    unittest.main()
