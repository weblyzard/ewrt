'''
Created on 21.06.2012

@author: Norman Suesstrunk, Heinz-Peter Lang

class for executing batch requests to the facebook api
'''
import unittest
import json
import urllib
import httplib
import logging
from ssl import SSLError

from eWRT.config import FACEBOOK_ACCESS_KEY
from eWRT.ws.facebook import FacebookWS

MAX_BATCH_SIZE = 3
TIMEOUT = 100 # timeout for the requests in seconds

logger = logging.getLogger('eWRT.ws.facebook')

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
        ''' executes the search 
        :param fbWSList: list of :class:eWRT.ws.facebook.FacebookWS object
        :type fbWSList: list
        :returns: result
        :rtype: list
        ''' 
        assert len(fbWSList), 'list of facebook services empty'

        result = []
        search_result = self._send_post(self.access_token, fbWSList)
        
        for row in search_result: 
            if not row: 
                logger.debug('row == %s ... continue' % row)
                continue
            
            data = json.loads(row['body'])
            
            if 'data' in data:    
                for post in json.loads(row['body'])['data']:
                    post['url'] = 'http://www.facebook.com/%s' % post['id']
                    result.append(post)
                    if 'comments' in post and 'data' in post['comments']:
                        for i, comment in enumerate(post['comments']['data']):
                            comment['type'] = 'comment'
                            comment['parent_url'] = post['url']
                            comment['url'] = '%s?comment=%s' % (post['url'], i)
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
        conn = httplib.HTTPSConnection(cls.faceBookGraphHost,
                                       timeout=TIMEOUT)
        all_batch_requests = cls._get_json_batch_request_string(fbWSList)
        
        for batch_requests in cls.get_batch(all_batch_requests):
            batch_requests = json.dumps(batch_requests)
            logger.debug('Making batch_requests with %s' % batch_requests)
            params = urllib.urlencode({cls.accessTokenHTTPParam: access_token,
                                       cls.batchHTTPParam: batch_requests})
            headers = {'Content-type': 'application/x-www-form-urlencoded',
                       'Accept': 'text/plain'}
            
            try: 
                
                conn.request('POST', '/', params, headers)
                response = conn.getresponse()
    
                data = json.loads(response.read())
    
                if isinstance(data, dict) and 'error' in data:
                    result.append(data)
                else: 
                    result.extend(data)

            except SSLError, e: 
                logger.error('Could not request: %s, %s' % (batch_requests, e))
            
        conn.close()
        return result
    
    @staticmethod
    def get_batch(requests, batch_size=MAX_BATCH_SIZE):
        for i in range(0, len(requests), batch_size):
            yield requests[i:i+batch_size]
            
class TestFacebookWS(unittest.TestCase):
    
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
        result = fbBatchRequest.run_search('107961012601035/feed', 
                                           objectType='path',
                                           limit=10)
        
        for x in result:
            print x
            
        assert len(result) >= 1

    def test_search(self):
        terms = ['Department of Health and Human Services', 'carcinomas', 
                 'National Oceanic and Atmospheric Administration', 'Mercedes-Benz',
                 'Audi', 'BMW', 'tumour', 'cancer', 'cop18', 'jane lubchenco', 'tumour', 'irgendwas']
        
        fbWSList = []
        
        for term in terms: 
            fbWSList.append(FacebookWS(term, 'post', 1353954200, 100))
        
        result = FbBatchRequest._send_post(fbWSList)
        print result
        print len(result)
        
if __name__ == "__main__":

    unittest.main()
