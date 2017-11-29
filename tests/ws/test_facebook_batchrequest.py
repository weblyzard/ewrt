#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from eWRT.ws.facebook.fbBatchRequest import FbBatchRequest
from eWRT.ws.facebook import FacebookWS


class TestFacebookBatchRequest(unittest.TestCase):
    
    def test_bad_request(self):
        access_token = "AAAElj9ZBZCquoBAGkKlcPvJsUCpyAZBxz6nsOYr8LAmpIj9Q9EZCKl9xVAYmlXGh2UQvhVellSWsZALPn6V73ZAZBiaxlwqkWlUjGVLzAHd7gZDZD"
        fbBatchRequest = FbBatchRequest(access_token)
        
        try: 
            fbBatchRequest.run_search('Linus Torvalds')
        except Exception as e: 
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
