'''
Created on 21.06.2012

@author: Norman Suesstrunk

class for executing batch requests to the facebook api
'''
import unittest
import json
import urllib
import httplib

from eWRT.config import FACEBOOK_ACCESS_KEY
from eWRT.ws.facebook import FacebookWS

MAX_BATCH_SIZE = 50

class FbBatchRequest(object):
    '''
    @class FacebookBatchRequest
    Class for sending batch requests to the facebook api
    the actual requests are constructed with objects from the FacebookWS class.  
    '''

    batchHTTPParam = 'batch' # http post parameter for the facebook batch http interface
    accessTokenHTTPParam = 'access_token'
    faceBookGraphHost = 'graph.facebook.com'

    def __init__(self, access_token=FACEBOOK_ACCESS_KEY):
        ''' Constructor '''
        self.access_token = access_token
    
    def run_search(self, terms, objectType='all', since=None, limit=None):
        ''' runs a batch search '''
        if not isinstance(terms, list):
            terms = [terms]

        return self.make_search([FacebookWS(term, objectType, 
                                            since, limit) for term in terms])

    def make_search(self, fbWSList):
        ''' ''' 
        assert len(fbWSList), 'list of facebook services empty'

        result = []
        search_result = self._send_post(self.access_token, fbWSList)
        
        for row in search_result: 
            if not row: 
                print 'row == %s ... continue' % row
                continue
            
            data = json.loads(row['body'])
            
            if 'data' in data:    
                for post in json.loads(row['body'])['data']:
                    result.append(post)
                    url = 'http://www.facebook.com/%s' % post['id'].replace('_', '/posts/')
                    if 'comments' in post and 'data' in post['comments']:
                        for comment in post['comments']['data']:
                            comment['type'] = 'comment'
                            comment['parent_url'] = url
                            comment['url'] = url
                            result.append(comment)
            elif data: 
                result.append(data)
                
        return result

    @classmethod
    def _get_json_batch_request_string(cls, fbWSList):
        '''
        delivers the json-string in the apropriate format for the facebook batch api
        '''
        return [fb.getJsonListStructure() for fb in fbWSList]
    
    @classmethod
    def _send_post(cls, access_token, fbWSList):
        '''
        sends the batch request as post to the facebook batch request api
        returns all the search results for the batch request
        '''
        result = []
        conn = httplib.HTTPSConnection(cls.faceBookGraphHost)
        all_batch_requests = cls._get_json_batch_request_string(fbWSList)
        
        for batch_requests in cls.get_batch(all_batch_requests):
            batch_requests = json.dumps(batch_requests)
            
            params = urllib.urlencode({cls.accessTokenHTTPParam: access_token,
                                       cls.batchHTTPParam: batch_requests})
            
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                       'Accept': 'text/plain'}
            
            conn.request('POST', '/', params, headers)
            response = conn.getresponse()

            data = json.loads(response.read())

            if isinstance(data, dict) and 'error' in data:
                result.append(data)
            else: 
                result.extend(data)
            
        conn.close()
        return result
    
    @staticmethod
    def get_batch(requests, batch_size=MAX_BATCH_SIZE):
        for i in range(0, len(requests), batch_size):
            yield requests[i:i+batch_size]
            
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
        result = fbBatchRequest.run_search('58220918250/feed', 
                                           objectType='path',
                                           limit=1)
        
        for x in result:
            print x
        assert len(result) >= 1
    
if __name__ == "__main__":

    unittest.main()
